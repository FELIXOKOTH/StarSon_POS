{ pkgs }:
{
  deps = [
    pkgs.python310Full
    pkgs.python310Packages.python-dotenv
  ];
}