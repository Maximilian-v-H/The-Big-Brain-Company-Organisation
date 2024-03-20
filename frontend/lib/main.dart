import 'package:flutter/material.dart';
import 'package:frontend/src/app.dart';
import 'package:go_router/go_router.dart';
import 'package:url_strategy/url_strategy.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  setPathUrlStrategy();
  GoRouter.optionURLReflectsImperativeAPIs = true;
  runApp(ProviderScope(observers: [Logger()], child: MyApp()));
}

class Logger extends ProviderObserver {
  @override
  void didUpdateProvider(ProviderBase provider, Object? oldValue,
      Object? newValue, ProviderContainer container) {
    debugPrint('Provider: $provider, OldValue: $oldValue, NewValue: $newValue');
  }
}
