import tobiiresearch.implementation
from tobiiresearch.interop import interop

# The following should match tobiiresearch.implementation.__all__
import tobiiresearch.implementation.DisplayArea
import tobiiresearch.implementation.Errors
import tobiiresearch.implementation.ExternalSignalData
import tobiiresearch.implementation.EyeImageData
import tobiiresearch.implementation.EyeTracker
import tobiiresearch.implementation.GazeData
import tobiiresearch.implementation.License
import tobiiresearch.implementation._LogEntry
import tobiiresearch.implementation.Notifications
import tobiiresearch.implementation.ScreenBasedCalibration
import tobiiresearch.implementation.StreamErrorData
import tobiiresearch.implementation.TimeSynchronizationData
import tobiiresearch.implementation.TrackBox
import tobiiresearch.implementation.HMDLensConfiguration
import tobiiresearch.implementation.UserPositionGuide
import tobiiresearch.implementation.Calibration
import tobiiresearch.implementation.StreamErrorData
import tobiiresearch.implementation.TimeSynchronizationData
import tobiiresearch.implementation.TrackBox
import tobiiresearch.implementation.HMDGazeData
import tobiiresearch.implementation.ScreenBasedCalibration
import tobiiresearch.implementation.HMDBasedCalibration
import tobiiresearch.implementation.ScreenBasedMonocularCalibration
import tobiiresearch.implementation.EyeOpennessData


# Make all globals in each module global in this module.
for module_name, module_content in tobiiresearch.implementation.__dict__.items():
    if module_name in tobiiresearch.implementation.__all__:
        for global_name, global_value in module_content.__dict__.items():
            if not global_name.endswith('__'):  # Don't import built in functionality.
                globals()[global_name] = global_value

__version__ = interop.get_sdk_version()

__copyright__ = '''
COPYRIGHT 2022 - PROPERTY OF TOBII AB
2022 TOBII AB - KARLSROVAGEN 2D, DANDERYD 182 53, SWEDEN - All Rights Reserved.

NOTICE:  All information contained herein is, and remains, the property of Tobii AB and its suppliers,
if any.  The intellectual and technical concepts contained herein are proprietary to Tobii AB and its suppliers and
may be covered by U.S.and Foreign Patents, patent applications, and are protected by trade secret or copyright law.
Dissemination of this information or reproduction of this material is strictly forbidden unless prior written
permission is obtained from Tobii AB.
'''

# Clean up so we don't export these internally used variables.
del module_name
del module_content
del global_name
del global_value
del tobiiresearch
del interop
