import threats
import analyze
import urls
import database

if __name__ == '__main__':
    # create lists to merge the received reports into one
    threats_objects = list()
    antivirus_bases_objects = list()
    network_attacks_objects = list()
    program_versions_objects = list()
    dynamic_objects = list()

    # THREATS
    # create class object and merge reports
    for path in urls.th_open_path:
        threats_objects.append(threats.ThreatsReport(path, urls.th_sheet_name))
    # (rework)  rewrite like same as above
    for obj in range(len(threats_objects)):
        threats_objects[obj].all_samples_threats()
        threats_objects[obj].save_result(urls.th_save_path[obj])
        print(threats_objects[obj])

    database.mongo_test()
    # # PROGRAM_VERSIONS
    # # create class object and merge reports
    # for path in urls.pv_open_path:
    #     program_versions_objects.append(program_versions.ProgramVersions(path, urls.pv_sheet_name))
    # # (rework) rewrite like same as above
    # for obj in range(len(program_versions_objects)):
    #     program_versions_objects[obj].all_samples_program_versions()
    #     program_versions_objects[obj].save_result(urls.pv_save_path[obj])
    #     print(program_versions_objects[obj])

    # # ANTIVIRUS_BASES
    # # create class object and merge reports
    # for path in urls.ab_open_path:
    #     antivirus_bases_objects.append(antivirus_bases.AntivirusBases(path, urls.ab_sheet_name))
    # # (rework) rewrite like same as above
    # for obj in range(len(antivirus_bases_objects)):
    #     antivirus_bases_objects[obj].all_samples_antivirus_bases()
    #     antivirus_bases_objects[obj].save_result(urls.ab_save_path[obj])
    #     print(antivirus_bases_objects[obj])

    # # NETWORK_ATTACKS
    # # create class object and merge reports
    # for path in urls.na_open_path:
    #     network_attacks_objects.append(network_attacks.NetworkAttacks(path, urls.na_sheet_name))
    # # (rework) rewrite like same as above
    # for obj in range(len(network_attacks_objects)):
    #     network_attacks_objects[obj].all_samples_network_attack()
    #     network_attacks_objects[obj].save_result(urls.na_save_path[obj])
    #     print(network_attacks_objects[obj])

    # dynamic report
    # create class object

    for path in urls.th_open_path:
        dynamic_objects.append(analyze.Analyzer(path, urls.th_sheet_name))
    for obj in range(len(dynamic_objects)):
        dynamic_objects[obj].all_samples_th(dynamic_objects)
        dynamic_objects[obj].save_result_th(urls.dsave_path_th[obj])
        print(dynamic_objects[obj])

    for path in urls.ab_open_path:
        dynamic_objects.append(analyze.Analyzer(path, urls.ab_sheet_name))
    for obj in range(len(dynamic_objects)):
        dynamic_objects[obj].all_samples_ab(dynamic_objects)
        dynamic_objects[obj].save_result_ab(urls.dsave_path_ab[obj])
        print(dynamic_objects[obj])
    #
    # dynamic_black_list = analyze.Analyzer()
    # dynamic_black_list.th_black_list(threats_objects)
    #
    # dynamic_types = analyze.Analyzer()
    # dynamic_types.th_types_summ(threats_objects)
    # dynamic_types.th_types_parts(threats_objects)
    #
    # dynamic_statuses = analyze.Analyzer()
    # # 2 samples in one xlsx (ab_statuses_summ + ab_statuses_parts)
    # dynamic_statuses.ab_statuses_dynamic(antivirus_bases_objects)
    # dynamic_statuses.ab_statuses_summ(antivirus_bases_objects)
