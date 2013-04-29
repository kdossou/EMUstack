""" None of the functions in this module deserve to live.

    Each should be made redundant and eliminated as soon as
    practicable.
"""

import numpy as np

def save_scat_mat(matrix, name, st, p, num_pw):
    # reshape matrices to be consistent with pcpv.exe output
    format_label_nu = '%04d' % st
    format_p        = '%04d' % p

    file_name = "st%(st)s_wl%(wl)s_%(mat_name)s" % {
        'st' : format_label_nu, 'wl' : format_p, 'mat_name' : name }
    np.save(file_name, matrix)
    # file_name = "st%(st)s_wl%(wl)s_%(mat_name)s.txt" % {
    #     'st' : format_label_nu, 'wl' : format_p, 'mat_name' : name }
    # with open(file_name, 'w') as outfile:
    #     for k in range(num_pw):
    #         for i in range(num_pw):
    #             data = [i+1,  k+1, np.real(matrix[i,k]), np.imag(matrix[i,k]),
    #                 np.abs(matrix[i,k])**2]
    #             data = np.reshape(data, (1,5))
    #             np.savetxt(outfile, data, fmt=['%4i','%4i','%25.17G','%25.17G','%25.17G'], delimiter='')

def load_scat_mat(name, st, p):
    # reshape matrices to be consistent with pcpv.exe output
    format_title = '%04d' % st
    format_p     = '%04d' % p

    file_name = "st%(st)s_wl%(wl)s_%(mat_name)s.npy" % {
        'st' : format_title, 'wl' : format_p, 'mat_name' : name }

    return np.mat(np.load(file_name))

def load_scat_mat_old(name, st, p):
    # reshape matrices to be consistent with pcpv.exe output
    format_title = '%04d' % st
    format_p     = '%04d' % p

    file_name = "st%(st)s_wl%(wl)s_%(mat_name)s.txt" % {
        'st' : format_title, 'wl' : format_p, 'mat_name' : name }
    data   = np.loadtxt(file_name)
    num_1  = max(data[:,0])
    num_2  = max(data[:,1])
    matrix = np.mat(data[:,2] + data[:,3]*(0+1j))
    matrix = np.reshape(matrix, (num_2, num_1))
    return matrix

def save_k_perps(anallo_list, num_pw):
    data_out = np.zeros((len(anallo_list), 2 + 2*len(anallo_list[0].beta)))

    #TODO: check that beta is the same length for everything
    #TODO: check that everything is the same label_nu and num_pw

    if num_pw != len(anallo_list[0].beta):
        raise ValueError, "Felix doesn't know what he's doing"

    for i, an in enumerate(anallo_list):
        data_out[i,:2] = (num_pw, an.light.Lambda)
        re, im = an.beta.real, an.beta.imag
        # beta = [beta[0].real, beta[0].imag, beta[1].real, ...]
        beta = np.vstack((re, im)).T.reshape(-1)
        data_out[i,2:] = beta

    filename = "beta_st%04d.txt" % an.structure.label_nu
    np.savetxt(filename, data_out, fmt='%25.17G', delimiter='')

def save_omegas(simmo_list):
    max_nval = max([s.nval for s in simmo_list])
    omega_out       = np.zeros((len(simmo_list), 5 + 2*max_nval))
    omega_pol_out   = np.zeros((len(simmo_list), 5 + max_nval))
    omega_fz_out    = np.zeros_like(omega_out)
    omega_ft_out    = np.zeros_like(omega_out)

    #TODO: check that everything has the same label_nu
    #TODO: rename goddamned omega to beta

    for i, s in enumerate(simmo_list):
        omega_out[i,:3]     = (s.nval, s.nval, s.light.Lambda)
        omega_out[i,3:5]    = s.bloch_vec() / (2*np.pi)
        omega_pol_out[i,:5] = omega_out[i,:5]
        omega_fz_out[i,:5]  = omega_out[i,:5]
        omega_ft_out[i,:5]  = omega_out[i,:5]

        omega_out[i,5:5+2*s.nval:2] = s.omega.real
        omega_out[i,6:6+2*s.nval:2] = s.omega.imag


        omega_pol_out[i,5:5+s.nval] = s.mode_pol[3].real

        # Collect the modes which have dominant z component (> 0.5)
        z_dom = abs(s.mode_pol[2]) > 0.5
        omega_fz_out[i,5:5+2*s.nval:2] = np.where(z_dom, s.omega.real, 0.)
        omega_fz_out[i,6:6+2*s.nval:2] = np.where(z_dom, s.omega.imag, 0.)

        # Collect the modes which are transverse-dominated
        t_dom = abs(s.mode_pol[2]) < 0.1
        omega_ft_out[i,5:5+2*s.nval:2] = np.where(t_dom, s.omega.real, 0.)
        omega_ft_out[i,6:6+2*s.nval:2] = np.where(t_dom, s.omega.imag, 0.)


    f_omega     = "omega_st%04d.txt"        % s.structure.label_nu
    f_omega_pol = "omega_pol_st%04d.txt"    % s.structure.label_nu
    f_omega_fz  = "omega_Fz_st%04d.txt"     % s.structure.label_nu
    f_omega_ft  = "omega_Ft_st%04d.txt"     % s.structure.label_nu
    
    np.savetxt(f_omega,     omega_out,      fmt='%25.17G', delimiter='')
    np.savetxt(f_omega_pol, omega_pol_out,  fmt='%25.17G', delimiter='')
    np.savetxt(f_omega_fz,  omega_fz_out,   fmt='%25.17G', delimiter='')
    np.savetxt(f_omega_ft,  omega_ft_out,   fmt='%25.17G', delimiter='')
