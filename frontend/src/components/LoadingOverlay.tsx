export default function LoadingOverlay() {
  return (
    <div className="fixed inset-0 z-[100] flex flex-col items-center justify-center bg-slate-900/70 glass-effect animate-[fadeIn_0.3s_ease-out]">
      <div role="status" aria-live="polite" className="bg-white rounded-2xl shadow-2xl p-8 max-w-sm text-center animate-[scaleIn_0.2s_ease-out] border border-slate-100">
        <div className="relative w-16 h-16 mx-auto mb-6">
          <div className="absolute inset-0 border-4 border-blue-100 rounded-full" />
          <div className="absolute inset-0 border-4 border-transparent border-t-blue-600 rounded-full animate-spin" />
          <div
            className="absolute inset-2 border-4 border-transparent border-t-indigo-400 rounded-full animate-spin"
            style={{ animationDirection: "reverse", animationDuration: "0.8s" }}
          />
        </div>
        <h3 className="text-lg font-bold text-slate-800 mb-2">Memproses Dokumen</h3>
        <p className="text-slate-500 text-sm leading-relaxed">
          Sedang memproses dokumen Anda...
          <br />
          <span className="font-semibold text-red-600">Mohon jangan tutup halaman ini.</span>
        </p>
      </div>
    </div>
  );
}
