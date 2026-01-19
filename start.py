# -*- coding: utf-8 -*-

import ipywidgets as ipw

template = """
<table>
<tr>
  <th style="text-align:center">🧪 Machine Learning Interatomic Potentials (MLIP)</th>
<tr>
  <td valign="top"><ul>
    <li><a href="{appbase}/main.ipynb" target="_blank">Launch MLIP App</a></li>
    <li><a href="{appbase}/example.ipynb" target="_blank">Simple Example</a></li>
    <li>Train and deploy ML potentials for molecular simulations</li>
  </ul></td>
</tr>
</table>
"""


def get_start_widget(appbase, jupbase, notebase):
    html = template.format(appbase=appbase, jupbase=jupbase, notebase=notebase)
    return ipw.HTML(html)


# EOF
