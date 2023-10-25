"""
Author: Zhongqiang (Richard) Ren
Version@2021-07
All Rights Reserved
ABOUT: this file constains CBSS-MCPF-AC, which is derived from CBSS (framework) and aim to solve MCPF-AC problems.
"""

import cbss
import seq_mcpf
from libmcpf import seq_mcpf_cbss


class CbssMCPF(cbss.CbssFramework) :
  """
  """
  def __init__(self, grids, starts, goals, dests, clusters, ac_dict, configs, spMat):
    """
    """
    # mtsp_solver = mcpf_seq.BridgeLKH_MCPF(grids, starts, goals, dests, ac_dict) # NOTE that ac_dict is only used in mtsp_solver, not in CBSS itself.
    # self.mtsp_solver = seq_mcpf_cbss.SeqMCPF(grids, starts, goals, dests, clusters, ac_dict, configs, spMat)
    # else:
    self.mtsp_solver = seq_mcpf.SeqMCPF(grids, starts, goals, dests, clusters, ac_dict, configs, spMat) # NOTE that ac_dict is only used in mtsp_solver, not in CBSS itself.
    super(CbssMCPF, self).__init__(self.mtsp_solver, grids, starts, goals, dests, dict(), configs)
    return

def RunCbssMCPF(grids, starts, targets, dests, clusters, ac_dict, configs, spMat):
  """
  starts, targets and dests are all node ID.
  heu_weight and prune_delta are not in use. @2021-05-26
  """
  ccbs_planner = CbssMCPF(grids, starts, targets, dests, clusters, ac_dict, configs, spMat)
  path_set, search_res = ccbs_planner.Search()
  num_nodes_in_transformed_graph = (ccbs_planner.mtsp_solver.get_num_nodes_transformed_graph()) - 2 * len(starts)
  # print(path_set)
  # print(res_dict)
  res_dict = dict()
  res_dict["path_set"] = path_set
  res_dict["round"] = search_res[0] # = num of high level nodes closed.
  res_dict["best_g_value"] = search_res[1]
  res_dict["num_nodes_transformed_graph"] = num_nodes_in_transformed_graph
  res_dict["open_list_size"] = search_res[3]
  res_dict["num_low_level_expanded"] = search_res[4]
  res_dict["search_success"] = search_res[5]
  res_dict["search_time"] = search_res[6]
  res_dict["n_tsp_call"] = search_res[7]
  res_dict["n_tsp_time"] = search_res[8]
  res_dict["n_roots"] = search_res[9]
  res_dict["cost_mat"] = ccbs_planner.mtsp_solver.cost_mat

  # if not test:
    # res_dict["cost_mat"]: ccbs_planner.mtsp_solver.cost_mat
  res_dict["target_assignment"] = ccbs_planner.mtsp_solver.target_assignment
  res_dict["cluster_target_selection"] = ccbs_planner.mtsp_solver.cluster_target_selection

  return res_dict
