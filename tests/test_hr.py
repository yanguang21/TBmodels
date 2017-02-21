#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>
# Date:    05.05.2015 13:59:00 CEST
# File:    hr_hamilton.py

from os.path import abspath, dirname, join

import pytest

import tbmodels
import numpy as np

kpt = [(0.1, 0.2, 0.7), (-0.3, 0.5, 0.2), (0., 0., 0.), (0.1, -0.9, -0.7)]

SAMPLE_DIR = join(dirname(abspath(__file__)), 'samples')

@pytest.mark.parametrize('hr_name', ['hr_hamilton.dat', 'wannier90_hr.dat', 'wannier90_hr_v2.dat'])
def test_hr(compare_data, hr_name):
    hr_file = join(SAMPLE_DIR, hr_name)
    model = tbmodels.Model.from_hr_file(hr_file, occ=28)
    H_list = np.array([model.hamilton(k) for k in kpt])

    compare_data(lambda x, y: np.isclose(x, y).all(), H_list)
        

@pytest.mark.parametrize('hr_name', ['wannier90_inconsistent.dat', 'wannier90_inconsistent_v2.dat'])
def test_inconsistent(hr_name):
    with pytest.raises(ValueError):
        model = tbmodels.Model.from_hr_file(join(SAMPLE_DIR, hr_name))


def test_emptylines():
    """test whether the input file with some random empty lines is correctly parsed"""
    model1 = tbmodels.Model.from_hr_file(join(SAMPLE_DIR, 'wannier90_hr.dat'))
    model2 = tbmodels.Model.from_hr_file(join(SAMPLE_DIR, 'wannier90_hr_v2.dat'))
    hop1 = model1.hop
    hop2 = model2.hop
    for k in hop1.keys() | hop2.keys():
        assert (np.array(hop1[k]) == np.array(hop2[k])).all()

def test_error():
    with pytest.raises(ValueError):
        tbmodels.Model.from_hr_file(join(SAMPLE_DIR, 'hr_hamilton.dat'), occ=28, pos=[[1., 1., 1.]])
