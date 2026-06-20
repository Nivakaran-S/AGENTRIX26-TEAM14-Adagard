// Citizen login / registration (NIC + password). Owner: Person B.
import 'package:flutter/material.dart';
import '../services/auth.dart';
import '../theme.dart';
import '../widgets/brand.dart';
import 'chat_screen.dart';

class AuthScreen extends StatefulWidget {
  const AuthScreen({super.key});
  @override
  State<AuthScreen> createState() => _AuthScreenState();
}

class _AuthScreenState extends State<AuthScreen> {
  final _auth = AuthService();
  final _nic = TextEditingController();
  final _name = TextEditingController();
  final _password = TextEditingController();
  bool _register = false;
  bool _busy = false;
  String? _error;

  Future<void> _submit() async {
    setState(() {
      _busy = true;
      _error = null;
    });
    final err = _register
        ? await _auth.register(_nic.text.trim(), _name.text.trim(), _password.text)
        : await _auth.login(_nic.text.trim(), _password.text);
    if (!mounted) return;
    if (err == null) {
      Navigator.of(context).pushReplacement(
        MaterialPageRoute(builder: (_) => const ChatScreen()),
      );
    } else {
      setState(() {
        _busy = false;
        _error = err;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24),
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 400),
            child: Container(
              decoration: BoxDecoration(
                color: GovColors.card,
                borderRadius: BorderRadius.circular(20),
                border: Border.all(color: GovColors.line),
              ),
              clipBehavior: Clip.antiAlias,
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Container(height: 3, color: GovColors.saffron),
                  Padding(
                    padding: const EdgeInsets.all(28),
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        const Align(alignment: Alignment.centerLeft, child: Wordmark(size: 30)),
                        const SizedBox(height: 18),
                        const Eyebrow('Citizen access'),
                        const SizedBox(height: 4),
                        Text(
                          _register ? 'Create your account' : 'Welcome back',
                          style: GovType.display(size: 26),
                        ),
                        const SizedBox(height: 22),
                        TextField(
                          controller: _nic,
                          decoration: const InputDecoration(labelText: 'NIC number'),
                        ),
                        if (_register) ...[
                          const SizedBox(height: 12),
                          TextField(
                            controller: _name,
                            decoration: const InputDecoration(labelText: 'Full name'),
                          ),
                        ],
                        const SizedBox(height: 12),
                        TextField(
                          controller: _password,
                          obscureText: true,
                          decoration: const InputDecoration(labelText: 'Password'),
                        ),
                        if (_error != null) ...[
                          const SizedBox(height: 14),
                          Text(_error!, style: const TextStyle(color: GovColors.garnet)),
                        ],
                        const SizedBox(height: 22),
                        FilledButton(
                          onPressed: _busy ? null : _submit,
                          child: Text(_busy ? 'Please wait…' : (_register ? 'Register' : 'Sign in')),
                        ),
                        TextButton(
                          onPressed: _busy ? null : () => setState(() => _register = !_register),
                          style: TextButton.styleFrom(foregroundColor: GovColors.garnet),
                          child: Text(_register
                              ? 'Have an account? Sign in'
                              : 'New here? Create an account'),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
