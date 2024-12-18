# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ImaerAutoCalc
                                 A QGIS plugin
 Automatically calculates sum and difference of two groups
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2023-10-03
        copyright            : (C) 2023 by Robin van Maaren
        email                : rvmrobin@gmai.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load ImaerAutoCalc class from file ImaerAutoCalc.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .ImaerAutoCalc import ImaerAutoCalc
    return ImaerAutoCalc(iface)
