// Backend client — matches /API_CONTRACT.md. Owner: Person B.
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'auth.dart';

/// Backend base URL. Defaults to the deployed Render backend; override for local
/// dev with --dart-define=API_BASE_URL=http://10.0.2.2:8000 (Android emulator).
const String kBaseUrl = String.fromEnvironment(
  'API_BASE_URL',
  defaultValue: 'https://govpath-backend.onrender.com',
);

/// Raised when the backend rejects the token (expired/invalid). The UI logs out.
class UnauthorizedException implements Exception {}

class GovPathApi {
  final AuthService _auth = AuthService();

  Future<Map<String, dynamic>> chat(String sessionId, String message, String lang) async {
    final token = await _auth.token();
    final res = await http.post(
      Uri.parse('$kBaseUrl/chat'),
      headers: {
        'Content-Type': 'application/json',
        if (token != null) 'Authorization': 'Bearer $token',
      },
      body: jsonEncode({'session_id': sessionId, 'message': message, 'lang': lang}),
    );
    if (res.statusCode == 401) {
      await _auth.logout();
      throw UnauthorizedException();
    }
    return jsonDecode(res.body) as Map<String, dynamic>;
  }
}
