#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "px4_ros2_cpp::px4_ros2_cpp" for configuration "Release"
set_property(TARGET px4_ros2_cpp::px4_ros2_cpp APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(px4_ros2_cpp::px4_ros2_cpp PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libpx4_ros2_cpp.so"
  IMPORTED_SONAME_RELEASE "libpx4_ros2_cpp.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS px4_ros2_cpp::px4_ros2_cpp )
list(APPEND _IMPORT_CHECK_FILES_FOR_px4_ros2_cpp::px4_ros2_cpp "${_IMPORT_PREFIX}/lib/libpx4_ros2_cpp.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
