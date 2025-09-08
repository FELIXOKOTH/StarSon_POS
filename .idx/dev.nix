# To learn more about how to use Nix to configure your environment
# see: https://firebase.google.com/docs/studio/customize-workspace
{ pkgs, ... }: {
  # Which nixpkgs channel to use.
  channel = "stable-24.05"; # or "unstable"

  # Use https://search.nixos.org/packages to find packages
  packages = [
    pkgs.python311
    pkgs.python311Packages.pip
    pkgs.python311Packages.flask
    pkgs.python311Packages.python-dotenv
    pkgs.flutter
    pkgs.firebase-tools
    pkgs.nodejs_20
    pkgs.docker
  ];

  # Sets environment variables in the workspace
  env = {};
  idx = {
    # Search for the extensions you want on https://open-vsx.org/ and use "publisher.id"
    extensions = [
      "dart-code.flutter"
      "ms-python.python"
    ];

    # Enable previews
    previews = {
      enable = true;
    };

    # Workspace lifecycle hooks
    workspace = {
      # Runs when a workspace is first created
      onCreate = {
      };
      # Runs when the workspace is (re)started
      onStart = {
      };
    };
  };
}
