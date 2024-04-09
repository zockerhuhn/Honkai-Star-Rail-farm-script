{pkgs}: {
  deps = [
    pkgs.python310Packages.xlib
    pkgs.xvfb-run
    pkgs.scrot
    pkgs.tesseract
  ];
}
