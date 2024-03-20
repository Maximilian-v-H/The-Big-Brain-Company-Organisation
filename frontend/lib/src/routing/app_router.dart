import 'package:frontend/src/home_page.dart';
import 'package:go_router/go_router.dart';

class AppRouting {
  static String home = "/";

  static GoRouter router = GoRouter(initialLocation: home, routes: <GoRoute>[
    GoRoute(
        path: home,
        name: home,
        builder: (context, state) => const HomePage(),
        routes: <GoRoute>[])
  ]);
}
