// GovPath brand theme — Sri Lankan civic. Garnet seal + saffron gold on gazette paper.
// Owner: Person B. Mirrors the admin web identity (Fraunces / Hanken Grotesk / Plex Mono).
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class GovColors {
  static const ink = Color(0xFF211A24);
  static const muted = Color(0xFF6A6270);
  static const garnet = Color(0xFF7A1631);
  static const garnetDeep = Color(0xFF5C0F24);
  static const saffron = Color(0xFFE0A22B);
  static const saffronSoft = Color(0xFFF7EAD0);
  static const palm = Color(0xFF0E6B5C);
  static const palmSoft = Color(0xFFDCEBE5);
  static const paper = Color(0xFFFAF5EC);
  static const card = Color(0xFFFFFFFF);
  static const line = Color(0xFFE7DECF);
}

class GovType {
  static TextStyle display({double size = 24, FontWeight weight = FontWeight.w600, Color color = GovColors.ink}) =>
      GoogleFonts.fraunces(fontSize: size, fontWeight: weight, color: color, letterSpacing: -0.2);

  static TextStyle mono({double size = 11, Color color = GovColors.muted, FontWeight weight = FontWeight.w500}) =>
      GoogleFonts.ibmPlexMono(fontSize: size, color: color, fontWeight: weight, letterSpacing: 1.2);
}

ThemeData govTheme() {
  final base = ThemeData.light(useMaterial3: true);
  final scheme = ColorScheme.fromSeed(
    seedColor: GovColors.garnet,
    brightness: Brightness.light,
  ).copyWith(
    primary: GovColors.garnet,
    secondary: GovColors.saffron,
    tertiary: GovColors.palm,
    surface: GovColors.card,
    onPrimary: GovColors.paper,
  );

  final textTheme = GoogleFonts.hankenGroteskTextTheme(base.textTheme)
      .apply(bodyColor: GovColors.ink, displayColor: GovColors.ink);

  return base.copyWith(
    colorScheme: scheme,
    scaffoldBackgroundColor: GovColors.paper,
    textTheme: textTheme,
    appBarTheme: const AppBarTheme(
      backgroundColor: GovColors.card,
      foregroundColor: GovColors.ink,
      surfaceTintColor: Colors.transparent,
      elevation: 0,
      scrolledUnderElevation: 0,
    ),
    inputDecorationTheme: InputDecorationTheme(
      filled: true,
      fillColor: GovColors.card,
      enabledBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(12),
        borderSide: const BorderSide(color: GovColors.line),
      ),
      focusedBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(12),
        borderSide: const BorderSide(color: GovColors.garnet, width: 1.6),
      ),
      labelStyle: const TextStyle(color: GovColors.muted),
    ),
    filledButtonTheme: FilledButtonThemeData(
      style: FilledButton.styleFrom(
        backgroundColor: GovColors.garnet,
        foregroundColor: GovColors.paper,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        padding: const EdgeInsets.symmetric(vertical: 16),
      ),
    ),
  );
}
