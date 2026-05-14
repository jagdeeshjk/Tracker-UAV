# CMake generated Testfile for 
# Source directory: /home/jagdeesh/tracker/src/vision_opencv/cv_bridge/test
# Build directory: /home/jagdeesh/tracker/build/cv_bridge/test
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(cv_bridge-utest "/usr/bin/python3" "-u" "/opt/ros/humble/share/ament_cmake_test/cmake/run_test.py" "/home/jagdeesh/tracker/build/cv_bridge/test_results/cv_bridge/cv_bridge-utest.gtest.xml" "--package-name" "cv_bridge" "--output-file" "/home/jagdeesh/tracker/build/cv_bridge/ament_cmake_gtest/cv_bridge-utest.txt" "--append-env" "LD_LIBRARY_PATH=/home/jagdeesh/tracker/build/cv_bridge/src" "--command" "/home/jagdeesh/tracker/build/cv_bridge/test/cv_bridge-utest" "--gtest_output=xml:/home/jagdeesh/tracker/build/cv_bridge/test_results/cv_bridge/cv_bridge-utest.gtest.xml")
set_tests_properties(cv_bridge-utest PROPERTIES  LABELS "gtest" REQUIRED_FILES "/home/jagdeesh/tracker/build/cv_bridge/test/cv_bridge-utest" TIMEOUT "60" WORKING_DIRECTORY "/home/jagdeesh/tracker/build/cv_bridge/test" _BACKTRACE_TRIPLES "/opt/ros/humble/share/ament_cmake_test/cmake/ament_add_test.cmake;125;add_test;/opt/ros/humble/share/ament_cmake_gtest/cmake/ament_add_gtest_test.cmake;86;ament_add_test;/opt/ros/humble/share/ament_cmake_gtest/cmake/ament_add_gtest.cmake;93;ament_add_gtest_test;/home/jagdeesh/tracker/src/vision_opencv/cv_bridge/test/CMakeLists.txt;16;ament_add_gtest;/home/jagdeesh/tracker/src/vision_opencv/cv_bridge/test/CMakeLists.txt;0;")
subdirs("../gtest")
