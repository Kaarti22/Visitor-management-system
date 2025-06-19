import { jwtDecode } from "jwt-decode";

interface TokenPayload {
  sub: string;
  id: number;
  exp: number;
}

export function getEmployeeFromToken(): TokenPayload | null {
  if (typeof window === "undefined") return null;
  const token = localStorage.getItem("token");
  if (!token) return null;

  try {
    const decoded = jwtDecode<TokenPayload>(token);
    return decoded;
  } catch (err) {
    console.error("Invalid token: ", err);
    return null;
  }
}
