// Citizen auth (NIC + password) with token kept in secure storage. Owner: Person B.
import 'dart:convert';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;
import 'api.dart' show kBaseUrl;

class AuthService {
  static const _storage = FlutterSecureStorage();
  static const _tokenKey = 'govpath_token';

  Future<String?> token() => _storage.read(key: _tokenKey);
  Future<bool> isLoggedIn() async => (await token()) != null;
  Future<void> logout() => _storage.delete(key: _tokenKey);

  /// Returns null on success (token stored), or an error message on failure.
  Future<String?> _auth(String path, Map<String, dynamic> body) async {
    try {
      final res = await http.post(
        Uri.parse('$kBaseUrl$path'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(body),
      );
      if (res.statusCode == 200 || res.statusCode == 201) {
        final data = jsonDecode(res.body) as Map<String, dynamic>;
        await _storage.write(key: _tokenKey, value: data['access_token'] as String);
        return null;
      }
      try {
        return (jsonDecode(res.body)['detail'] ?? 'Request failed').toString();
      } catch (_) {
        return 'Request failed (${res.statusCode})';
      }
    } catch (e) {
      return 'Could not reach the server';
    }
  }

  Future<String?> register(String nic, String fullName, String password) =>
      _auth('/auth/register', {'nic': nic, 'full_name': fullName, 'password': password});

  Future<String?> login(String nic, String password) =>
      _auth('/auth/login', {'nic': nic, 'password': password});
}
