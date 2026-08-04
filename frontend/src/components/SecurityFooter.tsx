import { ShieldCheck } from "lucide-react";

export default function SecurityFooter() {
  return (
    <div className="mt-8 bg-white rounded-xl border border-slate-200/80 p-6 text-center">
      <div className="flex items-center justify-center gap-2 mb-3">
        <ShieldCheck size={20} className="text-emerald-600" />
        <h4 className="font-bold text-slate-800 text-sm tracking-wide">
          PERNYATAAN KEAMANAN & PRIVASI DOKUMEN
        </h4>
      </div>
      <p className="text-slate-600 text-sm leading-relaxed max-w-3xl mx-auto">
        File PDF diproses secara aman di server dan dihapus segera setelah selesai.
        Tidak ada dokumen yang disimpan secara permanen. Setiap operasi tercatat
        dalam audit log untuk kepatuhan internal.
      </p>
      <p className="text-red-600 font-bold text-base tracking-wide mt-4">
        Say NO to I LOVE PDF / SMALL PDF
      </p>
    </div>
  );
}
