"use client";

import { useState, useEffect } from "react";
import { Shield, User } from "lucide-react";
import api from "@/lib/api";

interface UserRow {
  id: string;
  email: string;
  display_name: string;
  role: string;
  is_active: boolean;
  last_login_at: string | null;
  created_at: string | null;
}

export default function UserManagement() {
  const [users, setUsers] = useState<UserRow[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchUsers = async () => {
    try {
      const res = await api.get("/api/admin/users");
      setUsers(res.data.data);
    } catch {
      // handled by axios
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchUsers(); }, []);

  const handleUpgrade = async (userId: string, newRole: string) => {
    try {
      await api.post(`/api/admin/users/${userId}/upgrade?role=${newRole}`);
      setUsers((prev) => prev.map((u) => (u.id === userId ? { ...u, role: newRole } : u)));
    } catch {
      // silently fail
    }
  };

  if (loading) {
    return (
      <div className="bg-white rounded-2xl border border-slate-200/80 p-8 text-center">
        <div className="shimmer-bg h-6 w-48 mx-auto rounded" />
      </div>
    );
  }

  return (
    <div className="bg-white rounded-2xl border border-slate-200/80 shadow-sm overflow-hidden">
      <div className="px-6 py-5 border-b border-slate-100">
        <h2 className="text-lg font-bold text-slate-800">User Management</h2>
        <p className="text-xs text-slate-500">Kelola role user. User baru otomatis terdaftar sebagai regular user.</p>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm">
          <thead>
            <tr className="text-xs text-slate-500 uppercase bg-slate-50/80 border-b border-slate-200">
              <th className="px-6 py-3 font-semibold">User</th>
              <th className="px-6 py-3 font-semibold">Email</th>
              <th className="px-6 py-3 font-semibold">Role</th>
              <th className="px-6 py-3 font-semibold">Last Login</th>
              <th className="px-6 py-3 font-semibold text-right">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {users.map((u) => (
              <tr key={u.id} className="hover:bg-slate-50/50 transition-colors">
                <td className="px-6 py-3.5">
                  <div className="flex items-center gap-2">
                    <div className="w-7 h-7 rounded-full bg-gradient-to-br from-blue-400 to-indigo-500 text-white flex items-center justify-center text-xs font-bold">
                      {u.display_name.charAt(0).toUpperCase()}
                    </div>
                    <span className="font-medium text-slate-800 text-xs">{u.display_name}</span>
                  </div>
                </td>
                <td className="px-6 py-3.5 text-xs text-slate-600">{u.email}</td>
                <td className="px-6 py-3.5">
                  <span
                    className={`inline-flex items-center gap-1 px-2 py-1 text-[10px] font-bold rounded-lg ${
                      u.role === "admin"
                        ? "bg-purple-100 text-purple-700"
                        : "bg-slate-100 text-slate-600"
                    }`}
                  >
                    {u.role === "admin" ? <Shield size={10} /> : <User size={10} />}
                    {u.role.toUpperCase()}
                  </span>
                </td>
                <td className="px-6 py-3.5 text-xs text-slate-500">
                  {u.last_login_at ? new Date(u.last_login_at).toLocaleDateString("id-ID") : "-"}
                </td>
                <td className="px-6 py-3.5 text-right">
                  {u.role === "user" ? (
                    <button
                      onClick={() => handleUpgrade(u.id, "admin")}
                      className="text-xs font-medium text-purple-600 hover:text-purple-700 bg-purple-50 hover:bg-purple-100 px-3 py-1.5 rounded-lg transition-colors"
                    >
                      Upgrade ke Admin
                    </button>
                  ) : (
                    <button
                      onClick={() => handleUpgrade(u.id, "user")}
                      className="text-xs font-medium text-slate-500 hover:text-slate-700 bg-slate-50 hover:bg-slate-100 px-3 py-1.5 rounded-lg transition-colors"
                    >
                      Downgrade
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="px-6 py-3 text-center text-xs text-slate-400 border-t border-slate-100 bg-slate-50/30">
        {users.length} user terdaftar
      </div>
    </div>
  );
}
