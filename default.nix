
{system ? builtins.currentSystem} :

let pkgs = import <nixpkgs> { inherit system; };
in pkgs.stdenv.mkDerivation {
    Ut3 = pkgs.python3Packages.buildPythonPackage {
        name = "Ut3";
        src = ./.;
    };
}