#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

// Core SDK headers
#include "EDSDK.h"

// Controller & Model
#include "CameraController.h"
#include "CameraModel.h"
#include "CameraModelLegacy.h"
#include "CameraEvent.h"
#include "CameraEventListener.h"

// Command processing
#include "Processor.h"
#include "Command.h"

// Commands
#include "TakePictureCommand.h"
#include "StartEvfCommand.h"
#include "EndEvfCommand.h"
#include "SetPropertyCommand.h"
#include "GetPropertyCommand.h"
#include "GetPropertyDescCommand.h"
#include "SetCapacityCommand.h"
#include "SaveSettingCommand.h"
#include "PressShutterButtonCommand.h"
#include "OpenSessionCommand.h"
#include "CloseSessionCommand.h"
#include "NotifyCommand.h"
#include "DownloadEvfCommand.h"
#include "DownloadCommand.h"
#include "DriveLensCommand.h"
#include "DoEvfAFCommand.h"

// Utility classes
#include "Thread.h"
#include "Synchronized.h"
#include "Observer.h"
#include "ActionSource.h"
#include "ActionListener.h"
#include "ActionEvent.h"

// Property classes
#include "Tv.h"
#include "Av.h"
#include "Iso.h"
#include "MeteringMode.h"
#include "ImageQuality.h"
#include "ExposureComp.h"
#include "AEMode.h"
#include "EvfAFMode.h"
#include "PropertyComboBox.h"

namespace py = pybind11;

PYBIND11_MODULE(edsdk_bindings, m) {
    m.doc() = "Python bindings for Canon EDSDK";

    // ==========================================================================
    // 1. CORE CAMERA CONTROL
    // ==========================================================================
    
    // --- CameraModel ---
    py::class_<CameraModel, Observable>(m, "CameraModel")
        .def(py::init<EdsCameraRef>())
        .def("get_camera_object", &CameraModel::getCameraObject)
        // Property getters
        .def("get_ae_mode", &CameraModel::getAEMode)
        .def("get_tv", &CameraModel::getTv)
        .def("get_av", &CameraModel::getAv)
        .def("get_iso", &CameraModel::getIso)
        .def("get_metering_mode", &CameraModel::getMeteringMode)
        .def("get_exposure_compensation", &CameraModel::getExposureCompensation)
        .def("get_image_quality", &CameraModel::getImageQuality)
        .def("get_evf_mode", &CameraModel::getEvfMode)
        .def("get_evf_output_device", &CameraModel::getEvfOutputDevice)
        .def("get_evf_depth_of_field_preview", &CameraModel::getEvfDepthOfFieldPreview)
        .def("get_evf_zoom", &CameraModel::getEvfZoom)
        .def("get_evf_zoom_position", &CameraModel::getEvfZoomPosition)
        .def("get_evf_zoom_rect", &CameraModel::getEvfZoomRect)
        .def("get_evf_af_mode", &CameraModel::getEvfAFMode)
        .def("get_model_name", &CameraModel::getModelName)
        .def("get_focus_info", &CameraModel::getFocusInfo)
        // Property setters
        .def("set_ae_mode", &CameraModel::setAEMode)
        .def("set_tv", &CameraModel::setTv)
        .def("set_av", &CameraModel::setAv)
        .def("set_iso", &CameraModel::setIso)
        .def("set_metering_mode", &CameraModel::setMeteringMode)
        .def("set_exposure_compensation", &CameraModel::setExposureCompensation)
        .def("set_image_quality", &CameraModel::setImageQuality)
        .def("set_evf_mode", &CameraModel::setEvfMode)
        .def("set_evf_output_device", &CameraModel::setEvfOutputDevice)
        .def("set_evf_depth_of_field_preview", &CameraModel::setEvfDepthOfFieldPreview)
        .def("set_evf_zoom", &CameraModel::setEvfZoom)
        .def("set_evf_zoom_position", &CameraModel::setEvfZoomPosition)
        .def("set_evf_zoom_rect", &CameraModel::setEvfZoomRect)
        .def("set_evf_af_mode", &CameraModel::setEvfAFMode)
        .def("set_model_name", &CameraModel::setModelName)
        .def("set_focus_info", &CameraModel::setFocusInfo)
        // Property descriptions
        .def("get_property_desc", &CameraModel::getPropertyDesc)
        .def("set_property_desc", &CameraModel::setPropertyDesc)
        // Lock control
        .def("lock_ui", &CameraModel::lockUI)
        .def("unlock_ui", &CameraModel::unlockUI)
        // Camera operations
        .def("download_evf", &CameraModel::downloadEvf)
        .def("end_evf", &CameraModel::endEvf)
        .def("start_evf", &CameraModel::startEvf)
        .def("take_picture", &CameraModel::takePicture)
        .def("press_shutter_button", &CameraModel::pressShutterButton)
        .def("set_capacity", &CameraModel::setCapacity)
        .def("save_property", &CameraModel::saveProperty);
    
    // --- CameraController ---
    py::class_<CameraController, ActionListener>(m, "CameraController")
        .def(py::init<>())
        .def("set_camera_model", &CameraController::setCameraModel)
        .def("run", &CameraController::run)
        .def("action_performed", &CameraController::actionPerformed);

    // --- Processor ---
    py::class_<Processor, Thread>(m, "Processor")
        .def(py::init<>())
        .def("set_close_command", &Processor::setCloseCommand)
        .def("enqueue", &Processor::enqueue)
        .def("stop", &Processor::stop)
        .def("clear", &Processor::clear)
        .def("run", &Processor::run);

    // ==========================================================================
    // 2. COMMAND PATTERN CLASSES
    // ==========================================================================
    
    // --- Base Command ---
    py::class_<Command>(m, "Command")
        .def("execute", &Command::execute);

    // --- Camera Operation Commands ---
    py::class_<TakePictureCommand, Command>(m, "TakePictureCommand")
        .def(py::init<CameraModel*>());
        
    py::class_<PressShutterButtonCommand, Command>(m, "PressShutterButtonCommand")
        .def(py::init<CameraModel*, EdsUInt32>());
        
    py::class_<OpenSessionCommand, Command>(m, "OpenSessionCommand")
        .def(py::init<CameraModel*>());
        
    py::class_<CloseSessionCommand, Command>(m, "CloseSessionCommand")
        .def(py::init<CameraModel*>());
        
    py::class_<SaveSettingCommand, Command>(m, "SaveSettingCommand")
        .def(py::init<CameraModel*>());

    // --- EVF Commands ---
    py::class_<StartEvfCommand, Command>(m, "StartEvfCommand")
        .def(py::init<CameraModel*>());
        
    py::class_<EndEvfCommand, Command>(m, "EndEvfCommand")
        .def(py::init<CameraModel*>());
        
    py::class_<DownloadEvfCommand, Command>(m, "DownloadEvfCommand")
        .def(py::init<CameraModel*>());
        
    py::class_<DoEvfAFCommand, Command>(m, "DoEvfAFCommand")
        .def(py::init<CameraModel*, EdsPoint>());
        
    py::class_<DriveLensCommand, Command>(m, "DriveLensCommand")
        .def(py::init<CameraModel*, EdsUInt32>());

    // --- Property Commands ---
    // Note: SetPropertyCommand is templated, would need template specializations
    // This is a simplified version for common types
    py::class_<GetPropertyCommand, Command>(m, "GetPropertyCommand")
        .def(py::init<CameraModel*, EdsUInt32>());
        
    py::class_<GetPropertyDescCommand, Command>(m, "GetPropertyDescCommand") 
        .def(py::init<CameraModel*, EdsUInt32>());
        
    py::class_<SetCapacityCommand, Command>(m, "SetCapacityCommand")
        .def(py::init<CameraModel*, const EdsCapacity&>());
        
    py::class_<NotifyCommand, Command>(m, "NotifyCommand")
        .def(py::init<CameraModel*, const std::string&>());
        
    py::class_<DownloadCommand, Command>(m, "DownloadCommand")
        .def(py::init<CameraModel*, EdsBaseRef>());

    // ==========================================================================
    // 3. UTILITY CLASSES
    // ==========================================================================
    
    // --- Event Handling ---
    py::class_<ActionEvent>(m, "ActionEvent")
        .def(py::init<const std::string&>())
        .def(py::init<const std::string&, void*>())
        .def("get_action_command", &ActionEvent::getActionCommand)
        .def("get_arg", &ActionEvent::getArg);
        
    py::class_<ActionListener>(m, "ActionListener")
        .def("action_performed", &ActionListener::actionPerformed);
        
    py::class_<CameraEvent>(m, "CameraEvent")
        .def(py::init<const std::string&>())
        .def(py::init<const std::string&, void*>())
        .def("get_event", &CameraEvent::getEvent)
        .def("get_arg", &CameraEvent::getArg);
        
    py::class_<Observer>(m, "Observer")
        .def("update", &Observer::update);
        
    py::class_<Observable>(m, "Observable")
        .def("add_observer", &Observable::addObserver)
        .def("remove_observer", &Observable::removeObserver)
        .def("notify_observers", &Observable::notifyObservers);

    // --- Threading ---
    py::class_<Thread>(m, "Thread")
        .def("start", &Thread::start)
        .def("join", &Thread::join)
        .def("suspend", &Thread::suspend)
        .def("resume", &Thread::resume);
        
    py::class_<Synchronized>(m, "Synchronized")
        .def(py::init<>())
        .def("lock", &Synchronized::lock)
        .def("unlock", &Synchronized::unlock)
        .def("wait", &Synchronized::wait)
        .def("notify", &Synchronized::notify);

    // ==========================================================================
    // 4. PROPERTY/VALUE CLASSES
    // ==========================================================================
    
    // --- Camera Settings ---
    py::class_<Tv>(m, "Tv")
        .def_static("get_label", &Tv::getLabel);
        
    py::class_<Av>(m, "Av")
        .def_static("get_label", &Av::getLabel);
        
    py::class_<Iso>(m, "Iso")
        .def_static("get_label", &Iso::getLabel);
        
    py::class_<AEMode>(m, "AEMode")
        .def_static("get_label", &AEMode::getLabel);
        
    py::class_<MeteringMode>(m, "MeteringMode")
        .def_static("get_label", &MeteringMode::getLabel);
        
    py::class_<ExposureComp>(m, "ExposureComp")
        .def_static("get_label", &ExposureComp::getLabel);
        
    py::class_<ImageQuality>(m, "ImageQuality")
        .def_static("get_label", &ImageQuality::getLabel);
        
    py::class_<EvfAFMode>(m, "EvfAFMode")
        .def_static("get_label", &EvfAFMode::getLabel);

    // ==========================================================================
    // 5. EDSDK TYPES AND CONSTANTS
    // ==========================================================================
    
    // EdsError values
    py::enum_<EdsError>(m, "EdsError")
        .value("OK", EDS_ERR_OK)
        .value("UNIMPLEMENTED", EDS_ERR_UNIMPLEMENTED)
        .value("INTERNAL_ERROR", EDS_ERR_INTERNAL_ERROR)
        .value("MEM_ALLOC_FAILED", EDS_ERR_MEM_ALLOC_FAILED)
        .value("MEM_FREE_FAILED", EDS_ERR_MEM_FREE_FAILED)
        .value("OPERATION_CANCELLED", EDS_ERR_OPERATION_CANCELLED)
        .value("INCOMPATIBLE_VERSION", EDS_ERR_INCOMPATIBLE_VERSION)
        .value("NOT_SUPPORTED", EDS_ERR_NOT_SUPPORTED)
        .value("UNEXPECTED_EXCEPTION", EDS_ERR_UNEXPECTED_EXCEPTION)
        .value("PROTECTION_VIOLATION", EDS_ERR_PROTECTION_VIOLATION)
        .value("FILE_IO_ERROR", EDS_ERR_FILE_IO_ERROR)
        .value("DEVICE_NOT_FOUND", EDS_ERR_DEVICE_NOT_FOUND)
        .value("DEVICE_BUSY", EDS_ERR_DEVICE_BUSY)
        .value("DEVICE_INVALID", EDS_ERR_DEVICE_INVALID)
        .value("COMMUNICATION_ERROR", EDS_ERR_COMMUNICATION_ERROR)
        .value("SESSION_NOT_OPEN", EDS_ERR_SESSION_NOT_OPEN);
    
    // Camera commands
    py::enum_<EdsCameraCommand>(m, "EdsCameraCommand")
        .value("TAKE_PICTURE", kEdsCameraCommand_TakePicture)
        .value("SHUTTER_BUTTON_HALFWAY", kEdsCameraCommand_ShutterButton_Halfway)
        .value("SHUTTER_BUTTON_COMPLETELY", kEdsCameraCommand_ShutterButton_Completely)
        .value("SHUTTER_BUTTON_OFF", kEdsCameraCommand_ShutterButton_OFF);
    
    // Property IDs
    py::enum_<EdsPropertyID>(m, "EdsPropertyID")
        .value("PRODUCT_NAME", kEdsPropID_ProductName)
        .value("AE_MODE_SELECT", kEdsPropID_AEModeSelect)
        .value("DRIVE_MODE", kEdsPropID_DriveMode)
        .value("ISO_SPEED", kEdsPropID_ISOSpeed)
        .value("METERING_MODE", kEdsPropID_MeteringMode)
        .value("AF_MODE", kEdsPropID_AFMode)
        .value("AV", kEdsPropID_Av)
        .value("TV", kEdsPropID_Tv)
        .value("EXPOSURE_COMPENSATION", kEdsPropID_ExposureCompensation)
        .value("IMAGE_QUALITY", kEdsPropID_ImageQuality)
        .value("EVF_MODE", kEdsPropID_Evf_Mode)
        .value("EVF_OUTPUT_DEVICE", kEdsPropID_Evf_OutputDevice)
        .value("EVF_AF_MODE", kEdsPropID_Evf_AFMode);
        
    // EVF Drive Lens
    py::enum_<EdsEvfDriveLens>(m, "EdsEvfDriveLens")
        .value("NEAR_1", kEdsEvfDriveLens_Near1)
        .value("NEAR_2", kEdsEvfDriveLens_Near2)
        .value("NEAR_3", kEdsEvfDriveLens_Near3)
        .value("FAR_1", kEdsEvfDriveLens_Far1)
        .value("FAR_2", kEdsEvfDriveLens_Far2)
        .value("FAR_3", kEdsEvfDriveLens_Far3);
    
    // Structs
    py::class_<EdsPoint>(m, "EdsPoint")
        .def(py::init<>())
        .def_readwrite("x", &EdsPoint::x)
        .def_readwrite("y", &EdsPoint::y);
        
    py::class_<EdsSize>(m, "EdsSize")
        .def(py::init<>())
        .def_readwrite("width", &EdsSize::width)
        .def_readwrite("height", &EdsSize::height);
        
    py::class_<EdsRect>(m, "EdsRect")
        .def(py::init<>())
        .def_readwrite("point", &EdsRect::point)
        .def_readwrite("size", &EdsRect::size);
        
    py::class_<EdsCapacity>(m, "EdsCapacity")
        .def(py::init<>())
        .def_readwrite("number_of_free_clusters", &EdsCapacity::numberOfFreeClusters)
        .def_readwrite("bytes_per_cluster", &EdsCapacity::bytesPerCluster)
        .def_readwrite("reset", &EdsCapacity::reset);
} 