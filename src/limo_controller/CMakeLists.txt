catkin_install_python(PROGRAMS
  scripts/move_distance.py
  scripts/manual_control.py  # Adicione esta linha
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)