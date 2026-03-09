cmake_minimum_required(VERSION 3.0.2)
project(limo_controller)

find_package(catkin REQUIRED)

catkin_package()

catkin_install_python(PROGRAMS
  scripts/move_distance.py
  scripts/manual_control.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)