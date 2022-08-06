# { pkgs ? import <nixpkgs> {}, ... }:

let 
  
  pkgs = import <nixpkgs> {
    overlays = [

      (self: super: {

        python39Packages.pip = super.python39Packages.pip.overrideAttrs (
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
    python39
    python39Packages.pip
  ];

  shellHook = ''
    # Tells pip to put packages into $PIP_PREFIX instead of the usual locations.
    # See https://pip.pypa.io/en/stable/user_guide/#environment-variables.
    export PIP_PREFIX=$(pwd)/env/packages
    export PYTHONPATH="$PIP_PREFIX/${pkgs.python3.sitePackages}:$PYTHONPATH"
    export PATH="$PIP_PREFIX/bin:$PATH"
    unset SOURCE_DATE_EPOCH
    
    pip install -r requirements.txt
  '';


}




