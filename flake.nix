{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-utils, ... }@inputs:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
        };
        poetry2nix = inputs.poetry2nix.lib.mkPoetry2Nix { inherit pkgs; };
        poetryEnv = poetry2nix.mkPoetryEnv {
          projectDir = ./.;
          # editablePackageSources = {
          #   audio_analyzer = ./audio_analyzer;
          # };
          python = pkgs.python311;
          extraPackages = (ps: with ps; [ tkinter ]);
          overrides = poetry2nix.defaultPoetryOverrides.extend (self: super: {
            matplotlib = super.matplotlib.overrideAttrs (
              old: { enableTk = true; }
            );
            tk = super.tk.overridePythonAttrs (
              old: { buildInputs = (old.buildInputs or [ ]) ++ [ super.setuptools ]; }
            );
            audioread = super.audioread.overridePythonAttrs (
              old: { buildInputs = (old.buildInputs or [ ]) ++ [ super.flit-core ]; }
            );
            soxr = super.soxr.overridePythonAttrs (
              old: { buildInputs = (old.buildInputs or [ ]) ++ [ super.cython ]; }
            );
            speechrecognition = super.speechrecognition.overridePythonAttrs (
                old: { buildInputs = (old.buildInputs or [ ]) ++ [ super.setuptools ]; }
              );
          });
        };
      in
      rec {
        devShells.default = pkgs.mkShell rec {
          packages = with pkgs; [
            poetry
          ];
          buildInputs = with pkgs; [
            poetryEnv
            portaudio
          ];
          shellHook = ''
            export LD_LIBRARY_PATH="${pkgs.lib.makeLibraryPath buildInputs}:$LD_LIBRARY_PATH"
            alias pyright='poetry run -- pyright'
            alias pyright-langserver='poetry run -- pyright-langserver'
            export PYTHONPATH="$PWD"
          '';
        };
      });
}
