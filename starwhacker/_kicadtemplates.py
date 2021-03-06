# _kicadtemplates.py

# Stores the template strings for the kicad files

templates = {

'edge':
'''
(gr_line (start {} {}) (end {} {}) (angle 90) (layer Edge.Cuts) (width 0.15))''',

'openModule':
'''
(module {} (layer {}) (tedit {}) (tstamp {})
(at {} {})
(fp_text reference {} (at 3 2) (layer F.SilkS) hide
(effects (font (size 1 1) (thickness 0.15)))
)
(fp_text value {} (at 3 -2) (layer F.Fab)
(effects (font (size 1 1) (thickness 0.15) italic))
)
''',

'closeModule':
'''
)
''',

'TH_star':
'''
(pad {} thru_hole circle (at {} {}) (size {} {}) (drill {}) (layers *.Cu *.Mask)
(solder_mask_margin 0.05))''',

'SMD_star':
'''(pad {} smd circle (at {} {}) (size {} {}) (layers F.Cu F.Mask) (solder_mask_margin 0.02))
''',

'constellation_line':
'''(segment (start {0} {1}) (end {2} {3}) (width {4}) (layer F.Cu) (net 0))
(gr_line (start {0} {1}) (end {2} {3}) (angle 90) (layer F.Mask) (width {4}))
''',

'silk_line':
'''(fp_line (start {} {}) (end {} {}) (layer F.SilkS) (width 0.15))
''',

'silk_circle_back':
'''(fp_circle (center {0} {1}) (end {0} {2}) (layer B.SilkS) (width 0.2))
''',

'silk_text':
'''(fp_text user "{}" (at {} {}) (layer F.SilkS)
(effects (font (size {} {}) (thickness 0.15)))
)
''',

'silk_text_back':
'''(fp_text user "{}" (at {} {}) (layer B.SilkS)
(effects (font (size {} {}) (thickness 0.15)) (justify mirror))
)
''',

'silk_text_gr':
'''(gr_text "{}" (at {} {}) (layer F.SilkS)
(effects (font (size {} {}) (thickness 0.15)))
)
''',

'silk_text_back_gr':
'''(gr_text "{}" (at {} {}) (layer B.SilkS)
(effects (font (size {} {}) (thickness 0.15)) (justify mirror))
)
''',

'polygon':
'''
(fp_poly (pts {}) (layer F.Cu) (width 0.01))
''',

'header':
'''
(kicad_pcb (version 4) (host pcbnew 4.0.7)

(general
(links 0)
(no_connects 0)
(area 0 0 0 0)
(thickness 1.6)
(drawings 9)
(tracks 0)
(zones 0)
(modules 0)
(nets 1)
)

(page A3)
(title_block
(title "{}")
(date {})
(company Bespokh)
)

(layers
(0 F.Cu signal)
(31 B.Cu signal)
(32 B.Adhes user)
(33 F.Adhes user)
(34 B.Paste user)
(35 F.Paste user)
(36 B.SilkS user)
(37 F.SilkS user)
(38 B.Mask user)
(39 F.Mask user)
(40 Dwgs.User user)
(41 Cmts.User user)
(42 Eco1.User user)
(43 Eco2.User user)
(44 Edge.Cuts user)
(45 Margin user)
(46 B.CrtYd user)
(47 F.CrtYd user)
(48 B.Fab user)
(49 F.Fab user)
)

(setup
(last_trace_width 0.25)
(trace_clearance 0.2)
(zone_clearance 0.508)
(zone_45_only no)
(trace_min 0.2)
(segment_width 0.2)
(edge_width 0.15)
(via_size 0.6)
(via_drill 0.4)
(via_min_size 0.4)
(via_min_drill 0.3)
(uvia_size 0.3)
(uvia_drill 0.1)
(uvias_allowed no)
(uvia_min_size 0.2)
(uvia_min_drill 0.1)
(pcb_text_width 0.3)
(pcb_text_size 1.5 1.5)
(mod_edge_width 0.15)
(mod_text_size 1 1)
(mod_text_width 0.15)
(pad_size 1.524 1.524)
(pad_drill 0.762)
(pad_to_mask_clearance 0.2)
(aux_axis_origin 0 0)
(visible_elements FFFFFF7F)
(pcbplotparams
(layerselection 0x00030_80000001)
(usegerberextensions false)
(excludeedgelayer true)
(linewidth 0.150000)
(plotframeref false)
(viasonmask false)
(mode 1)
(useauxorigin false)
(hpglpennumber 1)
(hpglpenspeed 20)
(hpglpendiameter 15)
(hpglpenoverlay 2)
(psnegative false)
(psa4output false)
(plotreference true)
(plotvalue true)
(plotinvisibletext false)
(padsonsilk false)
(subtractmaskfromsilk false)
(outputformat 1)
(mirror false)
(drillshape 1)
(scaleselection 1)
(outputdirectory ""))
)

(net 0 "")

(net_class Default "This is the default net class."
(clearance 0.2)
(trace_width 0.25)
(via_dia 0.6)
(via_drill 0.4)
(uvia_dia 0.3)
(uvia_drill 0.1)
)''',

'ender':
''')
'''
}