{pkgs}: {
  deps = [
    pkgs.libGLU
    pkgs.libGL
    pkgs.python310Packages.xlib
    pkgs.xvfb-run
    pkgs.scrot
    pkgs.tesseract
  ];
}
