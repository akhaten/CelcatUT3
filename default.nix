{system ? builtins.currentSystem} :

let pkgs = import <nixpkgs> { inherit system; };
in pkgs.stdenv.mkDerivation {
    CelcatUT3 = pkgs.python3Packages.buildPythonPackage {
        name = "CelcatUT3";
        src = ./.;
    };
}
