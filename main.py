import threats
import program_versions
import antivirus_bases
import network_attacks
import analyze
import urls
import save

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
        save.MongoDumper.df_to_json(threats_objects[obj].dict,
                                    '{}_{}'.format(obj, threats_objects[obj].col_name))  # for mongo database
        # print(threats_objects[obj])

    # PROGRAM_VERSIONS
    # create class object and merge reports
    for path in urls.pv_open_path:
        program_versions_objects.append(program_versions.ProgramVersions(path, urls.pv_sheet_name))
    # (rework) rewrite like same as above
    for obj in range(len(program_versions_objects)):
        program_versions_objects[obj].all_samples_program_versions()
        program_versions_objects[obj].save_result(urls.pv_save_path[obj])
        save.MongoDumper.df_to_json(program_versions_objects[obj].dict,
                                    '{}_{}'.format(obj, program_versions_objects[obj].col_name))
        # print(program_versions_objects[obj])

    # ANTIVIRUS_BASES
    # create class object and merge reports
    for path in urls.ab_open_path:
        antivirus_bases_objects.append(antivirus_bases.AntivirusBases(path, urls.ab_sheet_name))
    # (rework) rewrite like same as above
    for obj in range(len(antivirus_bases_objects)):
        antivirus_bases_objects[obj].all_samples_antivirus_bases()
        antivirus_bases_objects[obj].save_result(urls.ab_save_path[obj])
        save.MongoDumper.df_to_json(antivirus_bases_objects[obj].dict,
                                    '{}_{}'.format(obj, antivirus_bases_objects[obj].col_name))  # for mongo database
        # print(antivirus_bases_objects[obj])

    # # NETWORK_ATTACKS
    # # create class object and merge reports
    # for path in urls.na_open_path:
    #     network_attacks_objects.append(network_attacks.NetworkAttacks(path, urls.na_sheet_name))
    # # (rework) rewrite like same as above
    # for obj in range(len(network_attacks_objects)):
    #     network_attacks_objects[obj].all_samples_network_attack()
    #     network_attacks_objects[obj].save_result(urls.na_save_path[obj])
    #     save.MongoDumper.df_to_json(network_attacks_objects[obj].dict,
    #                                 '{}_{}'.format(obj, network_attacks_objects[obj].col_name))  # for mongo database
    #     print(network_attacks_objects[obj])

    # # dynamic report
    # # create class object

    dynamic_th = analyze.Analyzer()
    dynamic_th.all_samples_th(threats_objects)
    dynamic_th.save_result_th(urls.dsave_path_th)
    save.MongoDumper.df_to_json(dynamic_th.dict, '{}_{}'.format('05', dynamic_th.col_name_th))

    dynamic_ab = analyze.Analyzer()
    dynamic_ab.all_samples_ab(antivirus_bases_objects)
    dynamic_ab.save_result_ab(urls.dsave_path_ab)
    save.MongoDumper.df_to_json(dynamic_ab.dict, '{}_{}'.format('05', dynamic_ab.col_name_ab))

