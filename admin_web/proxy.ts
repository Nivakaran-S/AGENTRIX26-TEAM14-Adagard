// Route gate (Next 16 renamed `middleware` -> `proxy`). Owner: Person C.
// Presence of the JWT cookie is required for every page except /login; role-level
// gating (e.g. /admin) is enforced server-side in the page + by the backend.
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

const TOKEN_COOKIE = "govpath_token";

export function proxy(request: NextRequest) {
  const token = request.cookies.get(TOKEN_COOKIE)?.value;
  const { pathname } = request.nextUrl;
  const isLogin = pathname === "/login";

  if (!token && !isLogin) {
    const url = request.nextUrl.clone();
    url.pathname = "/login";
    return NextResponse.redirect(url);
  }
  if (token && isLogin) {
    const url = request.nextUrl.clone();
    url.pathname = "/";
    return NextResponse.redirect(url);
  }
  return NextResponse.next();
}

export const config = {
  // Run on everything except API routes and static assets.
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
};
