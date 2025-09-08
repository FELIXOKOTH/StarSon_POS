{ pkgs }:
{
  deps = [
    pkgs.python310Full
    pkgs.python310Packages.python-dotenv
    pkgs.python310Packages.reportlab
    pkgs.python310Packages.svglib
    pkgs.python310Packages.lxml
    pkgs.python310Packages.requests
    pkgs.python310Packages.google-api-python-client
    pkgs.python310Packages.google-auth-httplib2
    pkgs.python310Packages.google-auth-oauthlib
  ];
}