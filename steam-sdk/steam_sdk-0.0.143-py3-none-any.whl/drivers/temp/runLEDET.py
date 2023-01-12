from postLEDET import Post_LEDET
from simLEDET import Sim_LEDET

class Run_LEDET:
    def __init__(self, magnet_name, model_no, LEDET_folder, magnet_inputs_path=''):
        self.magnet_name = magnet_name
        self.model_no = model_no
        self.LEDET_folder = LEDET_folder
        self.magnet_inputs_path = magnet_inputs_path

    def run_case(self, **kwargs):
        # determine t_PC
        sim = Sim_LEDET(self.magnet_name, -self.model_no, self.LEDET_folder, self.magnet_inputs_path)
        t_pre_calc, step = sim.get_pre_calc_timing()
        sim.gen_LEDET_input(t_pre_calc, [0, step, t_pre_calc+0.1], **kwargs)
        sim.prep_LEDET_files(**kwargs)
        sim.run_LEDET()
        post = Post_LEDET(self.magnet_name, -self.model_no, self.LEDET_folder, self.magnet_inputs_path)
        t_PC = post.calc_timing()
        if 'delete_mat_file' in kwargs:
            if kwargs['delete_mat_file']:
                post.delete_mat_file()
        print(f'Calculated t_PC: {t_PC}')
        # run actual simulation
        sim = Sim_LEDET(self.magnet_name, self.model_no, self.LEDET_folder, self.magnet_inputs_path)
        sim.gen_LEDET_input(t_PC, 'file', **kwargs)
        sim.prep_LEDET_files()
        sim.run_LEDET()
        post = Post_LEDET(self.magnet_name, self.model_no, self.LEDET_folder, self.magnet_inputs_path)
        post.save_key_vectors()
        post.plot_results(video=False, save=True, **kwargs)
        results = post.key_results()
        if 'delete_mat_file' in kwargs:
            if kwargs['delete_mat_file']:
                post.delete_mat_file()
        return results

    def run_c(self, **kwargs):
        post = Post_LEDET(self.magnet_name, self.model_no, self.LEDET_folder, self.magnet_inputs_path)
        return post.key_results_fake()

