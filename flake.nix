{
  description = "bases-page asFile() wikilink repro";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs =
    { nixpkgs, ... }:
    let
      forAllSystems = nixpkgs.lib.genAttrs [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];
    in
    {
      devShells = forAllSystems (
        system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
        in
        {
          # Quartz v5 needs node >= 22.
          default = pkgs.mkShell {
            packages = [
              pkgs.nodejs_24
              pkgs.git
            ];
          };
        }
      );
    };
}
