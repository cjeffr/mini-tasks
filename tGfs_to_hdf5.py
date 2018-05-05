import os
import h5py
import numpy as np
import glob

def convert_tgf_hdf5(file_loc, sitecount, output_name):
    """
    A function to convert text gauge files to hdf5 for portability

    Parameters
    ----------
    file_loc = location of the GeoClaw gauge files
    sitecount = the number of tide gauge locations in the setrun file
    output_name = what to call the output file

    Returns
    -------

    """



    #path = '/Users/jeffriesc/Desktop/Gf_nested'
    data = np.loadtxt(os.path.join(file_loc, '000', '000_00000.txt'))
    sitecount = sitecount
    #fault_numbers = range(0, 5)
    tsunami_dict = {}
    runup_sites_dict = {}

    output_file = h5py.File('{}.hdf5'.format(output_name), 'w')
    grp = output_file.create_group('GF')
    time_grp = output_file.create_group('time')
    time_data = time_grp.create_dataset('timedata', shape=(len(data),), dtype='f')
    time_data[...] = data[:,0]

    for root, dirs, filenames in os.walk(file_loc):
        for dir in dirs:
            tsunami_dict[dir] = np.zeros(shape=(len(data), sitecount))
            tsunami_dict['epoch'] = data[:,0]



        for fname in filenames:
            print(fname)
            if not fname[0] == '.':
                filename, file_extension = os.path.splitext(fname)
                number = os.path.basename(filename).split('_')
                subfault = number[0]
                site = int(number[1])
                array_index = None
                try:
                    array_index = runup_sites_dict[site]
                except:
                    array_index = len(runup_sites_dict)
                    runup_sites_dict[site] = array_index
                #output_file.create_group('{}/{}/{}'.format(grp, subfault, array_index))
                # dset = output_file.create_dataset('{}/{}/{:03}'.format(grp, subfault, array_index),
                #                                   shape=(len(data),),dtype='f')
                # dset = grp.create_dataset('{}/{:03}'.format(subfault, array_index), shape=(len(data),), dtype='f')
                with open (os.path.join(root, fname)) as f:
                    print(f)
                    data_from_file = np.loadtxt(f)


                    tsunami_dict[subfault][:, array_index] = data_from_file[:,1]

    for fault in tsunami_dict:
        if not fault == 'epoch':
            print(fault)
            print(tsunami_dict[fault])
            print(tsunami_dict[fault][:])
            dset = grp.create_dataset('{}'.format(fault), shape=(len(data), sitecount), dtype='f')
            dset[:, :] = tsunami_dict[fault]

    print('Done Loading!')

def create_txt_files(path, model, outpath):
    #def declare_gauge_output():
    out_path = outpath


    dirs = glob.glob(os.path.join(path, model,'GeoClawOutput', 'eq_*'))
    print(dirs)
    for dir in dirs:
       sf_number = dir[-3:]
       os.mkdir(os.path.join(out_path, sf_number))
       waveFiles = glob.glob('{}/gauge*.txt'.format(dir))
       gf_hash = {}
       for file in waveFiles:
           fname = os.path.basename(file)
           f = fname.split('.')
           loc_number = f[0][-5:]
           if loc_number not in gf_hash:
               gf_hash[loc_number] = []

           with open(file, 'r') as fh:

               next(fh)
               next(fh)
               for line in fh:
                   fields = line.split()
                   gf_hash[loc_number].append((fields[1], fields[5]))
       for gauge in gf_hash:
           print(sf_number, gauge)
           file_path = os.path.join(out_path, '{}'.format(sf_number), '{}_{}.txt'.format(sf_number, gauge))
           out_file = open(file_path, 'w')
           for pair in gf_hash[gauge]:
               out_file.write('{} {}\n'.format(pair[0], pair[1]))
           out_file.close()
   # print('Done!')

path = '/Users/jeffriesc/Data/AS_JAP/Catalog/GeoClawOutput'
model_name = 'AS_JAP'
gauge_loc = np.genfromtxt(os.path.join(path, '{}_gauges.txt'.format(model_name)),
                          delimiter='',skip_footer=1)


outpath = os.path.join(path, model_name, 'GF')


create_txt_files(path, model_name, outpath )

print(path + model_name)
convert_tgf_hdf5(path, len(gauge_loc), model_name)