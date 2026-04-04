import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export async function middleware(request: NextRequest) {
  const sessionToken = request.cookies.get("better-auth.session_token");
  const { pathname } = request.nextUrl;

  // 1. Authentication Check
  if (!sessionToken && !pathname.startsWith("/login")) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  // 2. Authorization (Role-Based) Simulation
  // In a production app, we would decode the session or hit an auth endpoint.
  // For now, we protect sensitive routes by assuming lack of session = no access.
  // Real security is enforced on the FastAPI backend via RoleChecker.
  
  const adminRoutes = ["/admin-reporting", "/audit"];
  const managerRoutes = ["/inventory", "/work-orders"];

  // If we had the role in a cookie, we could do:
  // const userRole = request.cookies.get("user_role")?.value;
  // if (adminRoutes.some(route => pathname.startsWith(route)) && userRole !== "ADMIN") {
  //   return NextResponse.redirect(new URL("/dashboard", request.url));
  // }

  return NextResponse.next();
}

export const config = {
  matcher: [
    "/dashboard/:path*",
    "/inventory/:path*",
    "/admin-reporting/:path*",
    "/work-orders/:path*",
  ],
};
