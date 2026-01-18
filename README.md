## Inspiration

<img width="1880" height="874" alt="image" src="https://github.com/user-attachments/assets/829aa4a0-abaa-41a5-86df-c7bbae600bbf" />


Building with LEGO is creative, but starting can be hard. Many people have loose bricks, limited time, or no idea what to build next. We wanted to remove that friction and turn constraints into creativity.  
**Bricked** was inspired by the idea that what you have should never limit what you can create. Instead, it should help define your identity as a builder.
---

## What it does

**Bricked** lets users upload a photo of their LEGO pieces and instantly see what they can build.

It:
- Detects and classifies LEGO pieces from an image  
- Tracks available inventory and used pieces  
- Generates builds using only the pieces the user has  
- Creates 3D previews and step-by-step build instructions  
- Adapts suggestions based on user history and preferences  

It helps children, parents, and builders with builder’s block get started and express themselves.

---

## How we built it

- OpenCV for piece detection and classification  
- FastAPI backend to manage scans, builds, and inventory  
- OpenSCAD to generate precise parametric LEGO models  
- LangGraph to coordinate multiple AI agents  
- Three.js for interactive 3D visualization  
- Next.js and React for the frontend  
- WebAssembly and Web Workers for fast in-browser compiling  
- Multiple LLMs specialized by task  

---

## Challenges we ran into

- Perspective distortion when estimating LEGO piece sizes  
- Accurately modeling real LEGO geometry in OpenSCAD  
- Reducing compile and render times for complex builds  
- Ensuring structural validity and correct piece counts  
- Coordinating multiple AI agents effectively  

---

## Accomplishments that we're proud of

- Scanning real LEGO piles into digital inventories  
- Running an OpenSCAD compiler directly in the browser  
- Building a working multi-agent planning system  
- Generating personalized, constraint-aware instructions  
- Creating a system that adapts to a builder’s identity over time  

---

## What we learned

- Constraints can increase creativity  
- Different AI models excel at different tasks  
- Performance is critical for usability  
- Translating physical objects into digital systems unlocks new possibilities  

---

## What's next for Bricked

- Improve piece detection accuracy  
- Speed up OpenSCAD compilation and rendering  
- Expand beyond LEGO to other building systems  
- Add AR previews for real-world guidance  
- Deploy and scale the platform for families and classrooms  
