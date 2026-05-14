# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_precision_land_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED precision_land_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(precision_land_FOUND FALSE)
  elseif(NOT precision_land_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(precision_land_FOUND FALSE)
  endif()
  return()
endif()
set(_precision_land_CONFIG_INCLUDED TRUE)

# output package information
if(NOT precision_land_FIND_QUIETLY)
  message(STATUS "Found precision_land: 0.0.1 (${precision_land_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'precision_land' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${precision_land_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(precision_land_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${precision_land_DIR}/${_extra}")
endforeach()
