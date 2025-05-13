#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <cstdint>

// Define to prevent MFC dependencies
#define NOAFX
#define NOMFC
#define SIMPLE_SDK_WRAPPER

// Core SDK headers
#include "EDSDK.h"

// Basic class definitions to replace the full implementation
namespace py = pybind11;

// Observer and Observable for event handling
class Observer {
public:
    virtual void update(void* event) {}
};

class Observable {
public:
    void addObserver(Observer* observer) {}
    void removeObserver(Observer* observer) {}
    void notifyObservers(void* event = nullptr) {}
};

// CameraModel must be defined before any class that uses it
class CameraModel {
public:
    CameraModel(uintptr_t camera) : camera_(reinterpret_cast<EdsCameraRef>(camera)) {}
    uintptr_t getCameraObject() const { return reinterpret_cast<uintptr_t>(camera_); }
    // Property getters - simplified stubs
    EdsUInt32 getAEMode() const { return 0; }
    EdsUInt32 getTv() const { return 0; }
    EdsUInt32 getAv() const { return 0; }
    EdsUInt32 getIso() const { return 0; }
    EdsUInt32 getMeteringMode() const { return 0; }
    EdsUInt32 getExposureCompensation() const { return 0; }
    EdsUInt32 getImageQuality() const { return 0; }
    EdsUInt32 getEvfMode() const { return 0; }
    EdsUInt32 getEvfOutputDevice() const { return 0; }
    EdsUInt32 getEvfDepthOfFieldPreview() const { return 0; }
    EdsUInt32 getEvfZoom() const { return 0; }
    EdsPoint getEvfZoomPosition() const { EdsPoint pt = {}; return pt; }
    EdsRect getEvfZoomRect() const { EdsRect rect = {}; return rect; }
    EdsUInt32 getEvfAFMode() const { return 0; }
    const char* getModelName() const { return "Camera"; }
    EdsUInt32 getFocusInfo() const { return 0; }
    // Property setters - simplified stubs
    void setAEMode(EdsUInt32 value) {}
    void setTv(EdsUInt32 value) {}
    void setAv(EdsUInt32 value) {}
    void setIso(EdsUInt32 value) {}
    void setMeteringMode(EdsUInt32 value) {}
    void setExposureCompensation(EdsUInt32 value) {}
    void setImageQuality(EdsUInt32 value) {}
    void setEvfMode(EdsUInt32 value) {}
    void setEvfOutputDevice(EdsUInt32 value) {}
    void setEvfDepthOfFieldPreview(EdsUInt32 value) {}
    void setEvfZoom(EdsUInt32 value) {}
    void setEvfZoomPosition(EdsPoint pt) {}
    void setEvfZoomRect(EdsRect rect) {}
    void setEvfAFMode(EdsUInt32 value) {}
    void setModelName(const char* name) {}
    void setFocusInfo(EdsUInt32 value) {}
    // Property descriptions - simplified stubs
    std::vector<EdsUInt32> getPropertyDesc(EdsUInt32 propertyID) { return {}; }
    void setPropertyDesc(EdsUInt32 propertyID, const std::vector<EdsUInt32>& desc) {}
    // Observer pattern methods
    void addObserver(Observer* observer) {}
    void removeObserver(Observer* observer) {}
    void notifyObservers(void* event = nullptr) {}
private:
    EdsCameraRef camera_;
};

// Action listener
class ActionEvent {
public:
    ActionEvent(const std::string& command) : command_(command), arg_(nullptr) {}
    ActionEvent(const std::string& command, void* arg) : command_(command), arg_(arg) {}
    
    const std::string& getActionCommand() const { return command_; }
    void* getArg() const { return arg_; }
    
private:
    std::string command_;
    void* arg_;
};

class ActionListener {
public:
    virtual void actionPerformed(const ActionEvent& event) {}
};

// Camera Controller
class CameraController : public ActionListener {
public:
    CameraController() {}
    void setCameraModel(CameraModel* model) {}
    void run() {}
    void actionPerformed(const ActionEvent& event) override {}
};

// Thread class
class Thread {
public:
    void start() {}
    void join() {}
    void suspend() {}
    void resume() {}
    virtual void run() {}
};

// Synchronized
class Synchronized {
public:
    void lock() {}
    void unlock() {}
    void wait() {}
    void notify() {}
};

// Command
class Command {
public:
    virtual bool execute() { return true; }
};

// Camera Event
class CameraEvent {
public:
    CameraEvent(const std::string& event) : event_(event), arg_(nullptr) {}
    CameraEvent(const std::string& event, void* arg) : event_(event), arg_(arg) {}
    
    const std::string& getEvent() const { return event_; }
    void* getArg() const { return arg_; }
    
private:
    std::string event_;
    void* arg_;
};

// Command Processor
class Processor : public Thread {
public:
    Processor() {}
    void setCloseCommand(Command* cmd) {}
    void enqueue(Command* cmd) {}
    void stop() {}
    void clear() {}
    void run() override {}
};

// Camera Commands
class TakePictureCommand {
public:
    TakePictureCommand(uintptr_t model) {}
    TakePictureCommand(uintptr_t model, const std::string& save_path) {}
    bool execute() { return true; }
};

class PressShutterButtonCommand {
public:
    PressShutterButtonCommand(uintptr_t model, EdsUInt32 params) {}
    bool execute() { return true; }
};

class OpenSessionCommand {
public:
    OpenSessionCommand(uintptr_t model) {}
    bool execute() { return true; }
};

class CloseSessionCommand {
public:
    CloseSessionCommand(uintptr_t model) {}
    bool execute() { return true; }
};

class SaveSettingCommand {
public:
    SaveSettingCommand(uintptr_t model) {}
    bool execute() { return true; }
};

class StartEvfCommand {
public:
    StartEvfCommand(uintptr_t model) {}
    bool execute() { return true; }
};

class EndEvfCommand {
public:
    EndEvfCommand(uintptr_t model) {}
    bool execute() { return true; }
};

class DownloadEvfCommand {
public:
    DownloadEvfCommand(uintptr_t model) {}
    bool execute() { return true; }
};

class DoEvfAFCommand {
public:
    DoEvfAFCommand(uintptr_t model, EdsPoint point) {}
    bool execute() { return true; }
};

class DriveLensCommand {
public:
    DriveLensCommand(uintptr_t model, EdsUInt32 param) {}
    bool execute() { return true; }
};

class GetPropertyCommand {
public:
    GetPropertyCommand(uintptr_t model, EdsUInt32 propertyID) {}
    bool execute() { return true; }
};

class GetPropertyDescCommand {
public:
    GetPropertyDescCommand(uintptr_t model, EdsUInt32 propertyID) {}
    bool execute() { return true; }
};

class SetCapacityCommand {
public:
    SetCapacityCommand(uintptr_t model, const EdsCapacity& capacity) {}
    bool execute() { return true; }
};

class NotifyCommand {
public:
    NotifyCommand(uintptr_t model, const std::string& notification) {}
    bool execute() { return true; }
};

class DownloadCommand {
public:
    DownloadCommand(uintptr_t model, uintptr_t baseRef) {}
    bool execute() { return true; }
};

// Property label classes
class Tv {
public:
    static const char* getLabel(EdsUInt32 value) { return ""; }
};

class Av {
public:
    static const char* getLabel(EdsUInt32 value) { return ""; }
};

class Iso {
public:
    static const char* getLabel(EdsUInt32 value) { return ""; }
};

class AEMode {
public:
    static const char* getLabel(EdsUInt32 value) { return ""; }
};

class MeteringMode {
public:
    static const char* getLabel(EdsUInt32 value) { return ""; }
};

class ExposureComp {
public:
    static const char* getLabel(EdsUInt32 value) { return ""; }
};

class ImageQuality {
public:
    static const char* getLabel(EdsUInt32 value) { return ""; }
};

class EvfAFMode {
public:
    static const char* getLabel(EdsUInt32 value) { return ""; }
};

// The actual Python module definition
PYBIND11_MODULE(edsdk_bindings, m) {
    m.doc() = "Python bindings for Canon EDSDK";

    // Core SDK functions
    m.def("EdsInitializeSDK", []() { return EdsInitializeSDK(); });
    m.def("EdsTerminateSDK", []() { return EdsTerminateSDK(); });
    m.def("EdsGetCameraList", []() -> uintptr_t {
        EdsCameraListRef cameraList = nullptr;
        EdsError err = EdsGetCameraList(&cameraList);
        return reinterpret_cast<uintptr_t>(cameraList);
    });
    m.def("EdsGetChildCount", [](uintptr_t ref) {
        EdsUInt32 count = 0;
        EdsError err = EdsGetChildCount(reinterpret_cast<EdsBaseRef>(ref), &count);
        return count;
    });
    m.def("EdsGetChildAtIndex", [](uintptr_t ref, EdsInt32 index) {
        EdsBaseRef childRef = nullptr;
        EdsError err = EdsGetChildAtIndex(reinterpret_cast<EdsBaseRef>(ref), index, &childRef);
        return reinterpret_cast<uintptr_t>(childRef);
    });
    m.def("EdsRelease", [](uintptr_t ref) {
        return EdsRelease(reinterpret_cast<EdsBaseRef>(ref));
    });

    // CameraModel class
    py::class_<CameraModel>(m, "CameraModel")
        .def(py::init<uintptr_t>())
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
        // Observer pattern methods
        .def("add_observer", &CameraModel::addObserver)
        .def("remove_observer", &CameraModel::removeObserver)
        .def("notify_observers", &CameraModel::notifyObservers);
    
    // CameraController
    py::class_<CameraController>(m, "CameraController")
        .def(py::init<>())
        .def("set_camera_model", &CameraController::setCameraModel)
        .def("run", &CameraController::run)
        .def("action_performed", &CameraController::actionPerformed);

    // Processor
    py::class_<Processor>(m, "Processor")
        .def(py::init<>())
        .def("set_close_command", &Processor::setCloseCommand)
        .def("enqueue", &Processor::enqueue)
        .def("stop", &Processor::stop)
        .def("clear", &Processor::clear)
        .def("run", &Processor::run);

    // Command classes
    py::class_<Command>(m, "Command")
        .def("execute", &Command::execute);

    py::class_<TakePictureCommand>(m, "TakePictureCommand")
        .def(py::init<uintptr_t>())
        .def(py::init<uintptr_t, const std::string&>())
        .def("execute", &TakePictureCommand::execute);
        
    py::class_<PressShutterButtonCommand>(m, "PressShutterButtonCommand")
        .def(py::init<uintptr_t, EdsUInt32>())
        .def("execute", &PressShutterButtonCommand::execute);
        
    py::class_<OpenSessionCommand>(m, "OpenSessionCommand")
        .def(py::init<uintptr_t>())
        .def("execute", &OpenSessionCommand::execute);
        
    py::class_<CloseSessionCommand>(m, "CloseSessionCommand")
        .def(py::init<uintptr_t>())
        .def("execute", &CloseSessionCommand::execute);
        
    py::class_<SaveSettingCommand>(m, "SaveSettingCommand")
        .def(py::init<uintptr_t>())
        .def("execute", &SaveSettingCommand::execute);

    py::class_<StartEvfCommand>(m, "StartEvfCommand")
        .def(py::init<uintptr_t>())
        .def("execute", &StartEvfCommand::execute);
        
    py::class_<EndEvfCommand>(m, "EndEvfCommand")
        .def(py::init<uintptr_t>())
        .def("execute", &EndEvfCommand::execute);
        
    py::class_<DownloadEvfCommand>(m, "DownloadEvfCommand")
        .def(py::init<uintptr_t>())
        .def("execute", &DownloadEvfCommand::execute);
        
    py::class_<DoEvfAFCommand>(m, "DoEvfAFCommand")
        .def(py::init<uintptr_t, EdsPoint>())
        .def("execute", &DoEvfAFCommand::execute);
        
    py::class_<DriveLensCommand>(m, "DriveLensCommand")
        .def(py::init<uintptr_t, EdsUInt32>())
        .def("execute", &DriveLensCommand::execute);

    py::class_<GetPropertyCommand>(m, "GetPropertyCommand")
        .def(py::init<uintptr_t, EdsUInt32>())
        .def("execute", &GetPropertyCommand::execute);
        
    py::class_<GetPropertyDescCommand>(m, "GetPropertyDescCommand") 
        .def(py::init<uintptr_t, EdsUInt32>())
        .def("execute", &GetPropertyDescCommand::execute);
        
    py::class_<SetCapacityCommand>(m, "SetCapacityCommand")
        .def(py::init<uintptr_t, const EdsCapacity&>())
        .def("execute", &SetCapacityCommand::execute);
        
    py::class_<NotifyCommand>(m, "NotifyCommand")
        .def(py::init<uintptr_t, const std::string&>())
        .def("execute", &NotifyCommand::execute);
        
    py::class_<DownloadCommand>(m, "DownloadCommand")
        .def(py::init<uintptr_t, uintptr_t>())
        .def("execute", &DownloadCommand::execute);

    // Utility classes
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
        .def(py::init<>())
        .def("update", &Observer::update);
        
    py::class_<Observable>(m, "Observable")
        .def(py::init<>())
        .def("add_observer", &Observable::addObserver)
        .def("remove_observer", &Observable::removeObserver)
        .def("notify_observers", &Observable::notifyObservers);

    py::class_<Thread>(m, "Thread")
        .def(py::init<>())
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

    // Camera settings classes
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

    // EDSDK enums and constants - using int values directly to avoid C++ enum issues
#ifdef EDS_ERR_OK
    m.attr("EDS_ERR_OK") = static_cast<int>(EDS_ERR_OK);
#endif
#ifdef EDS_ERR_UNIMPLEMENTED
    m.attr("EDS_ERR_UNIMPLEMENTED") = static_cast<int>(EDS_ERR_UNIMPLEMENTED);
#endif
#ifdef EDS_ERR_INTERNAL_ERROR
    m.attr("EDS_ERR_INTERNAL_ERROR") = static_cast<int>(EDS_ERR_INTERNAL_ERROR);
#endif
#ifdef EDS_ERR_MEM_ALLOC_FAILED
    m.attr("EDS_ERR_MEM_ALLOC_FAILED") = static_cast<int>(EDS_ERR_MEM_ALLOC_FAILED);
#endif
#ifdef EDS_ERR_MEM_FREE_FAILED
    m.attr("EDS_ERR_MEM_FREE_FAILED") = static_cast<int>(EDS_ERR_MEM_FREE_FAILED);
#endif
#ifdef EDS_ERR_OPERATION_CANCELLED
    m.attr("EDS_ERR_OPERATION_CANCELLED") = static_cast<int>(EDS_ERR_OPERATION_CANCELLED);
#endif
#ifdef EDS_ERR_INCOMPATIBLE_VERSION
    m.attr("EDS_ERR_INCOMPATIBLE_VERSION") = static_cast<int>(EDS_ERR_INCOMPATIBLE_VERSION);
#endif
#ifdef EDS_ERR_NOT_SUPPORTED
    m.attr("EDS_ERR_NOT_SUPPORTED") = static_cast<int>(EDS_ERR_NOT_SUPPORTED);
#endif
#ifdef EDS_ERR_UNEXPECTED_EXCEPTION
    m.attr("EDS_ERR_UNEXPECTED_EXCEPTION") = static_cast<int>(EDS_ERR_UNEXPECTED_EXCEPTION);
#endif
#ifdef EDS_ERR_PROTECTION_VIOLATION
    m.attr("EDS_ERR_PROTECTION_VIOLATION") = static_cast<int>(EDS_ERR_PROTECTION_VIOLATION);
#endif
#ifdef EDS_ERR_FILE_IO_ERROR
    m.attr("EDS_ERR_FILE_IO_ERROR") = static_cast<int>(EDS_ERR_FILE_IO_ERROR);
#endif
#ifdef EDS_ERR_DEVICE_NOT_FOUND
    m.attr("EDS_ERR_DEVICE_NOT_FOUND") = static_cast<int>(EDS_ERR_DEVICE_NOT_FOUND);
#endif
#ifdef EDS_ERR_DEVICE_BUSY
    m.attr("EDS_ERR_DEVICE_BUSY") = static_cast<int>(EDS_ERR_DEVICE_BUSY);
#endif
#ifdef EDS_ERR_DEVICE_INVALID
    m.attr("EDS_ERR_DEVICE_INVALID") = static_cast<int>(EDS_ERR_DEVICE_INVALID);
#endif
#ifdef EDS_ERR_COMMUNICATION_ERROR
    m.attr("EDS_ERR_COMMUNICATION_ERROR") = static_cast<int>(EDS_ERR_COMMUNICATION_ERROR);
#endif
#ifdef EDS_ERR_SESSION_NOT_OPEN
    m.attr("EDS_ERR_SESSION_NOT_OPEN") = static_cast<int>(EDS_ERR_SESSION_NOT_OPEN);
#endif
    
    // Camera commands
    m.attr("kEdsCameraCommand_TakePicture") = static_cast<int>(kEdsCameraCommand_TakePicture);
    m.attr("kEdsCameraCommand_ShutterButton_Halfway") = static_cast<int>(kEdsCameraCommand_ShutterButton_Halfway);
    m.attr("kEdsCameraCommand_ShutterButton_Completely") = static_cast<int>(kEdsCameraCommand_ShutterButton_Completely);
    m.attr("kEdsCameraCommand_ShutterButton_OFF") = static_cast<int>(kEdsCameraCommand_ShutterButton_OFF);
    
    // Property IDs
    m.attr("kEdsPropID_ProductName") = static_cast<int>(kEdsPropID_ProductName);
    m.attr("kEdsPropID_AEModeSelect") = static_cast<int>(kEdsPropID_AEModeSelect);
    m.attr("kEdsPropID_DriveMode") = static_cast<int>(kEdsPropID_DriveMode);
    m.attr("kEdsPropID_ISOSpeed") = static_cast<int>(kEdsPropID_ISOSpeed);
    m.attr("kEdsPropID_MeteringMode") = static_cast<int>(kEdsPropID_MeteringMode);
    m.attr("kEdsPropID_AFMode") = static_cast<int>(kEdsPropID_AFMode);
    m.attr("kEdsPropID_Av") = static_cast<int>(kEdsPropID_Av);
    m.attr("kEdsPropID_Tv") = static_cast<int>(kEdsPropID_Tv);
    m.attr("kEdsPropID_ExposureCompensation") = static_cast<int>(kEdsPropID_ExposureCompensation);
    m.attr("kEdsPropID_ImageQuality") = static_cast<int>(kEdsPropID_ImageQuality);
    m.attr("kEdsPropID_Evf_Mode") = static_cast<int>(kEdsPropID_Evf_Mode);
    m.attr("kEdsPropID_Evf_OutputDevice") = static_cast<int>(kEdsPropID_Evf_OutputDevice);
    m.attr("kEdsPropID_Evf_AFMode") = static_cast<int>(kEdsPropID_Evf_AFMode);
        
    // EVF Drive Lens
    m.attr("kEdsEvfDriveLens_Near1") = static_cast<int>(kEdsEvfDriveLens_Near1);
    m.attr("kEdsEvfDriveLens_Near2") = static_cast<int>(kEdsEvfDriveLens_Near2);
    m.attr("kEdsEvfDriveLens_Near3") = static_cast<int>(kEdsEvfDriveLens_Near3);
    m.attr("kEdsEvfDriveLens_Far1") = static_cast<int>(kEdsEvfDriveLens_Far1);
    m.attr("kEdsEvfDriveLens_Far2") = static_cast<int>(kEdsEvfDriveLens_Far2);
    m.attr("kEdsEvfDriveLens_Far3") = static_cast<int>(kEdsEvfDriveLens_Far3);
    
    // EDSDK structs
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
        .def_readwrite("bytes_per_sector", &EdsCapacity::bytesPerSector)
        .def_readwrite("reset", &EdsCapacity::reset);

    // Expose EdsPropertyID as a submodule/class
    py::module_ EdsPropertyID = m.def_submodule("EdsPropertyID");
    EdsPropertyID.attr("ISO_SPEED") = static_cast<int>(kEdsPropID_ISOSpeed);
    EdsPropertyID.attr("AV") = static_cast<int>(kEdsPropID_Av);
    EdsPropertyID.attr("TV") = static_cast<int>(kEdsPropID_Tv);
    // Add more as needed

    // Expose EdsEvfDriveLens as a submodule/class
    py::module_ EdsEvfDriveLens = m.def_submodule("EdsEvfDriveLens");
    EdsEvfDriveLens.attr("NEAR_1") = static_cast<int>(kEdsEvfDriveLens_Near1);
    EdsEvfDriveLens.attr("NEAR_2") = static_cast<int>(kEdsEvfDriveLens_Near2);
    EdsEvfDriveLens.attr("NEAR_3") = static_cast<int>(kEdsEvfDriveLens_Near3);
    EdsEvfDriveLens.attr("FAR_1") = static_cast<int>(kEdsEvfDriveLens_Far1);
    EdsEvfDriveLens.attr("FAR_2") = static_cast<int>(kEdsEvfDriveLens_Far2);
    EdsEvfDriveLens.attr("FAR_3") = static_cast<int>(kEdsEvfDriveLens_Far3);

    // Expose EdsCameraCommand as a submodule/class
    py::module_ EdsCameraCommand = m.def_submodule("EdsCameraCommand");
    EdsCameraCommand.attr("SHUTTER_BUTTON_HALFWAY") = static_cast<int>(kEdsCameraCommand_ShutterButton_Halfway);
    EdsCameraCommand.attr("SHUTTER_BUTTON_COMPLETELY") = static_cast<int>(kEdsCameraCommand_ShutterButton_Completely);
    EdsCameraCommand.attr("SHUTTER_BUTTON_OFF") = static_cast<int>(kEdsCameraCommand_ShutterButton_OFF);
    // Add more as needed
} 