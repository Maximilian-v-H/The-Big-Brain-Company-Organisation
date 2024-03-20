import 'package:flutter/material.dart';
// ignore: depend_on_referenced_packages
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:frontend/src/constants/design.dart';
import 'package:frontend/src/routing/app_router.dart';

class MyApp extends ConsumerWidget {
  MyApp({super.key});
  final navigatorKey = GlobalKey<NavigatorState>();

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return MaterialApp.router(
      title: 'Test',
      debugShowCheckedModeBanner: false,
      localizationsDelegates: const [
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      supportedLocales: const [
        Locale('de', 'DE'),
        Locale('en', 'US'),
      ],
      theme: ThemeData(
          scaffoldBackgroundColor: Colors.white,
          iconTheme: const IconThemeData(color: black),
          textTheme: const TextTheme(
            displayLarge: TextStyle(
              fontSize: h1,
              color: black,
              fontWeight: FontWeight.bold,
            ),
            displayMedium: TextStyle(
              fontSize: h2,
              color: black,
              fontWeight: FontWeight.bold,
            ),
            displaySmall: TextStyle(
              fontSize: h3,
              color: black,
              fontWeight: FontWeight.bold,
            ),
            headlineLarge: TextStyle(
              fontSize: h4,
              color: black,
              fontWeight: FontWeight.bold,
            ),
            headlineMedium: TextStyle(
              fontSize: h5,
              color: black,
              fontWeight: FontWeight.bold,
            ),
            headlineSmall: TextStyle(
              fontSize: h6,
              color: black,
              fontWeight: FontWeight.bold,
            ),
            titleLarge: TextStyle(
              fontSize: h7,
              color: black,
              fontWeight: FontWeight.bold,
            ),
            titleMedium: TextStyle(
              fontSize: h7,
              color: black,
              fontWeight: FontWeight.bold,
            ),
            bodyLarge: TextStyle(
              fontSize: paragraph,
              color: black,
              fontWeight: FontWeight.normal,
            ),
            bodyMedium: TextStyle(
              fontSize: h7,
              color: black,
              fontWeight: FontWeight.normal,
            ),
            bodySmall: TextStyle(
              fontSize: 11,
              color: black,
              fontWeight: FontWeight.normal,
            ),
            labelLarge: TextStyle(
              fontSize: h5,
              color: black,
              fontWeight: FontWeight.normal,
            ),
            labelMedium: TextStyle(
              fontSize: h6,
              color: black,
              fontWeight: FontWeight.normal,
            ),
            labelSmall: TextStyle(
              fontSize: h7,
              color: black,
              fontWeight: FontWeight.normal,
            ),
          )),
      routerDelegate: AppRouting.router.routerDelegate,
      routeInformationParser: AppRouting.router.routeInformationParser,
      routeInformationProvider: AppRouting.router.routeInformationProvider,
    );
  }
}
