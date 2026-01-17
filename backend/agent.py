from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain.messages import HumanMessage, AIMessage, AnyMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Literal

# Graph state
class State(TypedDict):
    user_request: AnyMessage
    pieces_list: str
    build_plan: str
    feedback: str
    grade: str
    final_script: str

# Schema for structured output to use in evaluation
class Feedback(BaseModel):
    grade: Literal["pass", "fail"] = Field(
        description="Decide if the build plan is adequate.",
    )
    feedback: str = Field(
        description="If the build plan is not adequate, provide feedback on how to improve it.",
    )

# Agent functions
def architect_agent(state: State):
    msg = ''
    if state.get("feedback"):
        msg = llm.invoke(f"You are a structural analysis agent who architects lego builds. Rework the build plan \"{state['build_plan']}\" but take into account the feedback: \"{state['feedback']}\". Given the user request: \"{state['user_request'].content}\", provide a list of necessary structures for this build (e.g. a house build may need walls, a chimney, etc. depending on the pieces the user has). Carefully consider the number of pieces available: {state['pieces_list']}. Return the list with the structures as a comma-separated string and after each structure, include in parentheses the exact number of pieces and which pieces are needed for that structure and a concise description of how the pieces should be connected. Ensure the total number of pieces does not exceed the available pieces.")
    else:
        msg = llm.invoke(f"You are a structural analysis agent who architects lego builds. Given the user request: \"{state['user_request'].content}\", provide a list of necessary structures for this build (e.g. a house build may need walls, a chimney, etc. depending on the pieces the user has). Carefully consider the number of pieces available: {state['pieces_list']}. Return the list with the structures as a comma-separated string and after each structure, include in parentheses the exact number of pieces and which pieces are needed for that structure and a concise description of how the pieces should be connected. Ensure the total number of pieces does not exceed the available pieces.")
    
    summarized_msg = llm.invoke("Only return the final list of this response. The list should contain the structures as a comma-separated string and after each structure, it should include in parentheses the exact number of pieces and which pieces are needed for that structure. The message: " + msg.content)
    print("A")
    return {"build_plan": summarized_msg.content}

def evaluator_agent(state: State):
    grade = evaluator.invoke(f"You are a lego build evaluator. Given the user request: \"{state['user_request'].content}\", and the build plan: \"{state['build_plan']}\", ensure the quality of the build plan. First, verify that the build plan addresses the user request adequately. Next, check that the build plan is feasible given the pieces available: {state['pieces_list']} and that it uses exactly the given pieces or less. Finally, check if the build plan physically makes sense. That is, can all the pieces connect to eachother and can each structure connect to eachother without falling apart? Evaluate the build plan in this way.")
    print("B")
    return {"grade": grade.grade, "feedback": grade.feedback}

def builder_agent(state: State):
    msg = llm_reasoning.invoke(f"You are a lego build agent. Given the user request: \"{state['user_request'].content}\", and the build plan: \"{state['build_plan']}\", generate an OpenSCAD script to create the lego build. Ensure the script uses only the pieces available: {state['pieces_list']}. Return only the OpenSCAD script without any additional text.")
    summarized_msg = llm.invoke(f"Only return the final OpenSCAD script of this response. The message: " + msg.content)
    print("C")
    return {"final_script": summarized_msg.content}

# Conditional edge function
def route_evaluator(state: State):
    if state["grade"] == "pass":
        return "Accepted"
    elif state["grade"] == "fail":
        return "Rejected + Feedback"
    

load_dotenv()
llm = ChatGroq(
    model="llama-3.3-70b-versatile"
)
llm_reasoning = ChatGroq(
    model="qwen/qwen3-32b",
    max_retries=2,
)
evaluator = llm.with_structured_output(Feedback)

state_graph = StateGraph(State)
state_graph.add_node("architect_agent", architect_agent)
state_graph.add_node("evaluator_agent", evaluator_agent)
state_graph.add_node("builder_agent", builder_agent)

state_graph.add_edge(START, "architect_agent")
state_graph.add_edge("architect_agent", "evaluator_agent")
state_graph.add_conditional_edges(
    "evaluator_agent",
    route_evaluator,
    {  
        "Accepted": "builder_agent",
        "Rejected + Feedback": "architect_agent",
    },
)
state_graph.add_edge("builder_agent", END)

workflow = state_graph.compile()
state = workflow.invoke(
    {"user_request": HumanMessage(content="Build me a small house with a red roof using the pieces I have."),
     "pieces_list": "20 red 2x4 bricks, 15 white 2x2 bricks, 10 transparent 1x2 bricks, 5 black 1x4 bricks"}
)

print(state["build_plan"])
print(state["final_script"])