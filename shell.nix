{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
  buildInputs = [
    pkgs.python3
    pkgs.python3Packages.flask
    pkgs.python3Packages.matplotlib
    pkgs.python3Packages.reportlab
    pkgs.python3Packages.svglib
    pkgs.python3Packages.lxml
    pkgs.python3Packages.requests
    pkgs.python3Packages.google-api-python-client
    pkgs.python3Packages.google-auth-httplib2
    pkgs.python3Packages.google-auth-oauthlib
  ];
}
