import glob
import os
import sys
import pandas as pd

atext = 'dms_'
argn = len(sys.argv)
if argn >= 2:
    atext = sys.argv[1]
folders = glob.glob(r'%s*' % atext)  # glob.glob('dsm_*')
print(folders)

m_data = pd.read_table(folders[0] + r'/DMS_mobile/clusters12.dat', sep=' ')
m_data.columns = ['T', 'LC', 'LC_std', 'SLC',
                  'SLC_std', 'Rg', 'Rg_std', 'Pspan']
m_sfp_data = pd.read_table(folders[0] + r'/DMS_mobile/sfp.dat', sep=' ')
m_sfp_data.columns = ['T', 'sigma', 'sigma_std',
                      'fp', 'fp_std', 'p', 'p_std', 'Sm', 'Sm_std']

im_data = pd.read_table(
    folders[0] + r'/DMS_immobile/clusters_im_12.dat', sep=' ')
im_data.columns = ['T', 'LC', 'LC_std',
                   'SLC', 'SLC_std', 'Rg', 'Rg_std', 'Pspan']
im_sfp_data = pd.read_table(folders[0] + r'/DMS_immobile/sfp.dat', sep=' ')
im_sfp_data.columns = ['T', 'sigma', 'sigma_std',
                       'fp', 'fp_std', 'p', 'p_std', 'Sm', 'Sm_std']

for fd in folders[1:]:
    print(fd)
    if not os.path.isfile(fd + r'/DMS_mobile/clusters12.dat'):
        continue
    m_cur = pd.read_table(fd + r'/DMS_mobile/clusters12.dat', sep=' ')
    m_cur.columns = ['T', 'LC', 'LC_std', 'SLC',
                     'SLC_std', 'Rg', 'Rg_std', 'Pspan']
    m_data = pd.concat([m_data, m_cur])

    m_sfp_cur = pd.read_table(fd + r'/DMS_mobile/sfp.dat', sep=' ')
    m_sfp_cur.columns = ['T', 'sigma', 'sigma_std',
                         'fp', 'fp_std', 'p', 'p_std', 'Sm', 'Sm_std']
    m_sfp_data = pd.concat([m_sfp_data, m_sfp_cur])

    im_cur = pd.read_table(fd + r'/DMS_immobile/clusters_im_12.dat', sep=' ')
    im_cur.columns = ['T', 'LC', 'LC_std', 'SLC',
                      'SLC_std', 'Rg', 'Rg_std', 'Pspan']
    im_data = pd.concat([im_data, im_cur])

    im_sfp_cur = pd.read_table(fd + r'/DMS_immobile/sfp.dat', sep=' ')
    im_sfp_cur.columns = ['T', 'sigma', 'sigma_std',
                          'fp', 'fp_std', 'p', 'p_std', 'Sm', 'Sm_std']
    im_sfp_data = pd.concat([im_sfp_data, im_sfp_cur])

m_data = m_data.sort_values(by='T')
m_sfp_data = m_sfp_data.sort_values(by='T')
im_data = im_data.sort_values(by='T')
im_sfp_data = im_sfp_data.sort_values(by='T')

m_mean = m_data.groupby(['T'], as_index=False).mean()
m_mean.columns = ['T', 'LC', 'LC_std', 'SLC',
                  'SLC_std', 'Rg', 'Rg_std', 'Pspan']
m_sfp_mean = m_sfp_data.groupby(['T'], as_index=False).mean()
m_sfp_mean.columns = ['T', 'sigma', 'sigma_std',
                      'fp', 'fp_std', 'p', 'p_std', 'Sm', 'Sm_std']
im_mean = im_data.groupby(['T'], as_index=False).mean()
im_mean.columns = ['T', 'LC', 'LC_std',
                   'SLC', 'SLC_std', 'Rg', 'Rg_std', 'Pspan']
im_sfp_mean = im_sfp_data.groupby(['T'], as_index=False).mean()
im_sfp_mean.columns = ['T', 'sigma', 'sigma_std',
                       'fp', 'fp_std', 'p', 'p_std', 'Sm', 'Sm_std']

m_mean.to_csv('mean_dms_mobile.dat', float_format='%.5f', sep='\t', index=None)
m_sfp_mean.to_csv('mean_dms_mobile_sfp.dat',
                  float_format='%.5f', sep='\t', index=None)
im_mean.to_csv('mean_dms_immobile.dat',
               float_format='%.5f', sep='\t', index=None)
im_sfp_mean.to_csv('mean_dms_immobile_sfp.dat',
                   float_format='%.5f', sep='\t', index=None)
