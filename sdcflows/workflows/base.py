#!/usr/bin/env python
# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""
Base fieldmap estimation
------------------------

* Subject can have no data for fieldmap estimation - unwarping should not modify
  the images.
* Subject can have phase-difference data.
* Subject can have a fieldmap acquisition.
* Subject can have :abbr:`pepolar (Phase-Encoding POLArity)` image series for a
  phase-encoding based estimation.
* Subject can have two or three of the above - return average.


"""
from __future__ import print_function, division, absolute_import, unicode_literals

def fmap_estimator(fmap_bids, settings=None):
    """
    This workflow selects the fieldmap estimation data available for the subject and
    returns the estimated fieldmap in mm, along with a corresponding reference image.
    Current implementation applies the first type of fieldmap estimation found in the
    following order of precedence:

      * "Natural" fieldmaps
      * Phase-difference fieldmaps
      * PEPolar fieldmaps.


    Outputs:

        fmap
          The estimated fieldmap itself IN UNITS OF Hz.
        fmap_ref
          the anatomical reference for the fieldmap (magnitude image, corrected SEm, etc.)
        fmap_mask
          a brain mask for the fieldmap


    """

    # pybids type options: (phase1|phase2|phasediff|epi|fieldmap)
    # https://github.com/INCF/pybids/blob/213c425d8ee820f4b7a7ae96e447a4193da2f359/bids/grabbids/bids_layout.py#L63
    if fmap_bids['type'] == 'fieldmap':
        from .fmap import fmap_workflow
        fmapwf = fmap_workflow(settings=settings)
        # set inputs
        fmapwf.inputs.inputnode.fieldmap = fmap_bids['fieldmap']
        fmapwf.inputs.inputnode.magnitude = fmap_bids['magnitude']
        return fmapwf

    if fmap_bids['type'] == 'phasediff':
        from .phdiff import phdiff_workflow
        phwf = phdiff_workflow(settings=settings)
        # set inputs
        phwf.inputs.inputnode.phasediff = fmap_bids['phasediff']
        phwf.inputs.inputnode.magnitude = [
            fmap_bids['magnitude1'],
            fmap_bids['magnitude2']
        ]
        return phwf

    if fmap_bids['type'] in ['phase1', 'phase2', 'epi']:
        raise NotImplementedError
