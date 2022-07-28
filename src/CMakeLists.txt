set(dir "${CMAKE_CURRENT_SOURCE_DIR}")
list(
  APPEND
  srcs
  ${dir}/api.f90 # Added for libdlfind
  ${dir}/dl-find.f90
  ${dir}/dlf_allocate.f90
  ${dir}/dlf_checkpoint.f90
  ${dir}/dlf_conint.f90
  ${dir}/dlf_convergence.f90
  ${dir}/dlf_coords.f90
  ${dir}/dlf_dimer.f90
  ${dir}/dlf_formstep.f90
  ${dir}/dlf_global_module.f90
  ${dir}/dlf_hdlc_constraint.f90
  ${dir}/dlf_hdlc_hdlclib.f90
  ${dir}/dlf_hdlc_interface.f90
  ${dir}/dlf_hdlc_matrixlib.f90
  ${dir}/dlf_hdlc_primitive.f90
  ${dir}/dlf_lbfgs.f90
  ${dir}/dlf_linalg.f90
  ${dir}/dlf_microiter.f90
  ${dir}/dlf_neb.f90
  ${dir}/dlf_parallel_opt.f90
  ${dir}/dlf_qts.f90
  ${dir}/dlf_scalestep.f90
  ${dir}/dlf_serial.f90
  ${dir}/dlf_sort.f90
  ${dir}/dlf_stat_module.f90
  ${dir}/dlf_task.f90
  ${dir}/dlf_time.f90
  ${dir}/dlf_util.f90
# ${dir}/draw.f90
# ${dir}/main.f90
  ${dir}/mod_api.f90 # Added for libdlfind
  ${dir}/mod_globals.f90 # Added for libdlfind
)

set(srcs
    ${srcs}
    PARENT_SCOPE)
