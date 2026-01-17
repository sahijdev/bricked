"use client";
import { useEffect, useRef } from "react";
import {
  AmbientLight,
  BoxGeometry,
  Color,
  DirectionalLight,
  Mesh,
  MeshStandardMaterial,
  PerspectiveCamera,
  Scene,
  WebGLRenderer,
} from "three";

export default function ModelPage() {
  const mountRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    const mountEl = mountRef.current;
    if (!mountEl) return;

    const scene = new Scene();
    scene.background = new Color("#0f172a");

    const camera = new PerspectiveCamera(75, 1, 0.1, 1000);
    camera.position.z = 3;

    const renderer = new WebGLRenderer({ antialias: true });
    renderer.setPixelRatio(window.devicePixelRatio);
    mountEl.appendChild(renderer.domElement);

    const cube = new Mesh(
      new BoxGeometry(),
      new MeshStandardMaterial({ color: "#38bdf8", metalness: 0.1, roughness: 0.7 })
    );
    scene.add(cube);

    const ambient = new AmbientLight("#ffffff", 0.6);
    const directional = new DirectionalLight("#ffffff", 0.8);
    directional.position.set(2, 2, 3);
    scene.add(ambient, directional);

    const resize = () => {
      const size = Math.min(window.innerWidth - 48, 520);
      renderer.setSize(size, size);
      camera.aspect = 1;
      camera.updateProjectionMatrix();
    };
    resize();
    window.addEventListener("resize", resize);

    let animationFrame: number;
    const animate = () => {
      cube.rotation.x += 0.01;
      cube.rotation.y += 0.01;
      renderer.render(scene, camera);
      animationFrame = requestAnimationFrame(animate);
    };
    animate();

    return () => {
      cancelAnimationFrame(animationFrame);
      window.removeEventListener("resize", resize);
      mountEl.removeChild(renderer.domElement);
      renderer.dispose();
      cube.geometry.dispose();
      (cube.material as MeshStandardMaterial).dispose();
    };
  }, []);

  return (
    <main className="min-h-screen bg-slate-900 p-10 text-white">
      <h1 className="text-3xl font-semibold mb-6">Model workspace</h1>
      <div className="flex flex-col items-center gap-6">
        <div ref={mountRef} className="flex items-center justify-center rounded-2xl border border-slate-700 bg-slate-800/60 p-4 shadow-lg" />
        {/* Drop zone and UI go here */}
      </div>
    </main>
  );
}
