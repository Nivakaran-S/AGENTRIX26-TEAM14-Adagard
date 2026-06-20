// GovPath app entry. Owner: Person B.
import 'package:flutter/material.dart';
import 'services/auth.dart';
import 'screens/auth_screen.dart';
import 'screens/chat_screen.dart';
import 'theme.dart';

void main() => runApp(const GovPathApp());

class GovPathApp extends StatelessWidget {
  const GovPathApp({super.key});

  @override
  Widget build(BuildContext context) => MaterialApp(
        title: 'GovPath',
        debugShowCheckedModeBanner: false,
        theme: govTheme(),
        home: const RootGate(),
      );
}

/// Decides the first screen based on whether a citizen token is stored.
class RootGate extends StatelessWidget {
  const RootGate({super.key});
  @override
  Widget build(BuildContext context) {
    return FutureBuilder<bool>(
      future: AuthService().isLoggedIn(),
      builder: (context, snap) {
        if (!snap.hasData) {
          return const Scaffold(body: Center(child: CircularProgressIndicator()));
        }
        return snap.data! ? const ChatScreen() : const AuthScreen();
      },
    );
  }
}
