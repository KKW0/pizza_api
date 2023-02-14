"""
**Introduce**
A Python library for get a hierarchy tree dictionary or save json file of selected type objects
in selected model in present Maya scene using in Maya 2020 script editor.

**License**
Netflix VFX Academy
RAPA
Original work Copyright (c) 2022 Jo Ahyeon

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

**Get a Hierarchy of selected object**

Support for:

* Maya 2020
* Python 2.7
* Object Type:
    "camera", "cluster", "curve", "curveOnSurface", "emitter", "ikHandle", "imagePlane",
    "joint", "lattice", "nParticle", "particle", "plane", "rigidBody", "sculpt", "spring",
    "stroke", "subdiv"

**get_model**

:class:
'get_model.GetModelInformation' makes dictionary of selected model's selected type objects.

Example 1)
Get a Dictionary of Joint Objects  in 'pCylinder1' Using get_hierarchy_dict(str)
When a User Calls get_hierarchy_dict(str), It Shows the Dictionary in Readable Format.

.. doctest::
    gmi = GetModelInformation()
    gmi.model = 'pCylinder1'
    my_dict = gmi.get_hierarchy_dict('joint')

    Output >>
    {u'|pCylinder1|transform1|joint1': {u'joint2': {},
                                        u'joint3': {u'joint4': {}},
                                        u'joint5': {u'joint6': {},
                                                    u'joint7': {u'joint8': {}}}}}

Example 2)
Make Json file of Joint Objects in 'pCylinder1' Using get_hierarchy_dict(str)

.. doctest::
    gmi = GetModelInformation()
    gmi.model = 'pCylinder1'
    my_dict = gmi.get_hierarchy_dict('joint')
    gmi.make_json(my_dict)

    Output >>
    File saved at /home/rapa/model_dict_pCylinder1_joint.json
"""