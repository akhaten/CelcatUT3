
{system ? builtins.currentSystem} :

let pkgs = import <nixpkgs> { inherit system; };

in pkgs.python310Packages.buildPythonPackage {
	name = "Ut3";
	src = ./.;
	propagatedBuildInputs = with pkgs; [
		python310
		python310Packages.requests
		python310Packages.python-dateutil
		python310Packages.parse
	];
	doCheck = false;
}
