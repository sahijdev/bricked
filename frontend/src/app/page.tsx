"use client";
import { useState } from "react";
import DropZone from "./DropZone";

export default function ModelPage() {
  //const url = "https://api.brickognize.com/predict/";
  const url = "http://0.0.0.0:8000/detect";
  const [prompt, setPrompt] = useState("");

  async function sendFileToServer(file: File) {
    const formData = new FormData();
    formData.append("file", file); 
    const result = await fetch(url, {
      method: "POST",
      body: formData,
    });
    // This code works, but detects a single lego brick only, trying to pass to backend to extract individual lego bricks
    /*
    const result = await fetch(url, {
      method: "POST",
      body: formData,
    }).then((res) => res.json()).then((data) => {
      console.log("Server response:", data);
      const brickType = data.items[0].name;
      console.log(brickType);
      return data;
    })
      */
  }

  return (
    <main className="min-h-screen bg-slate-900 p-10 text-white">
      <h1 className="text-3xl font-semibold mb-6 text-center">Upload your Lego Inventory</h1>
      <div className="flex flex-col items-center gap-4">
        <DropZone onFiles={(file) => sendFileToServer(file)}/>
        <label className="w-full max-w-xl text-sm text-zinc-300">
          What do you want to build?
          <textarea
            className="mt-2 w-full rounded-xl border border-zinc-600 bg-zinc-800 p-3 text-white outline-none transition focus:border-blue-400 focus:ring focus:ring-blue-500/30"
            rows={3}
            placeholder="Describe the model you want (e.g., small spaceship, bridge, house)..."
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
          />
        </label>
        <button className="bg-green-500 p-3 rounded-md w-50 text-wh">Submit</button>
        </div>
    </main>
  );
}
