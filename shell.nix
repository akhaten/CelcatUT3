let 
  
  pkgs = import <nixpkgs> {
    overlays = [

      (self: super: {

        python310Packages.pip = super.python310Packages.pip.overrideAttrs (
          old : {
            src = super.fetchFromGitHub {
              owner = "pypa";
              repo = "pip";
              rev = "22.2.2";
              sha256 = "SLjmxFUFmvgy8E8kxfc6lxxCRo+GN4L77pqkWkRR8aE=";
            };
          }
        );

      })

    ];
  };

in
pkgs.mkShell {

  buildInputs = with pkgs; [
    python310
    python310Packages.pip
  ];

  shellHook = ''
    export PIP_PREFIX=$(pwd)/venv
    export PYTHONPATH="$PIP_PREFIX/${pkgs.python310.sitePackages}:$PYTHONPATH"
    export PATH="$PIP_PREFIX/bin:$PATH"
    unset SOURCE_DATE_EPOCH
  '';


}
