#!/usr/bin/env python3
dictTagToPath = {'FBM_VORONOI': 'shaders/features/fbm_voronoi.fs',
'RANDOM_3D': 'shaders/utils/random.fs',
'NOISE_GRADIENT_2D': 'shaders/utils/gradient.fs',
'RANDOM_2D': 'shaders/utils/random.fs',
'NOISE_VORONOI_2D': 'shaders/utils/voronoi.fs',
'PLATEAU': 'shaders/features/plateau.fs',
'FBM_GRADIENT': 'shaders/features/fbm_gradient.fs'}

dictFeatureFunctionToTag = {'fbm_voronoi': 'FBM_VORONOI',
'fbm_gradient': 'FBM_GRADIENT',
'plateau': 'PLATEAU'}