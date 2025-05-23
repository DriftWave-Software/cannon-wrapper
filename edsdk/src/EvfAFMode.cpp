/******************************************************************************
*                                                                             *
*   PROJECT : EOS Digital Software Development Kit EDSDK                      *
*      NAME : EvfAFMode.cpp                                                   *
*                                                                             *
*   Description: This is the Sample code to show the usage of EDSDK.          *
*                                                                             *
*                                                                             *
*******************************************************************************
*                                                                             *
*   Written and developed by Camera Design Dept.53                            *
*   Copyright Canon Inc. 2006-2008 All Rights Reserved                        *
*                                                                             *
*******************************************************************************/

#include "stdafx.h"
#include "CameraControl.h"
#include "EvfAFMode.h"

#define WM_USER_PROPERTY_CHANGED		WM_APP+1
#define WM_USER_PROPERTYDESC_CHANGED	WM_APP+2
// CEvfAFMode

IMPLEMENT_DYNAMIC(CEvfAFMode, CPropertyComboBox)
CEvfAFMode::CEvfAFMode()
{
	// set up action command
	setActionCommand("set_EvfAFMode");

	// Map of value and display name
	_propertyTable.insert( std::pair<EdsUInt32, const char *>(0x00,"Quick mode"));
	_propertyTable.insert( std::pair<EdsUInt32, const char *>(0x01,"1-point AF"));
	_propertyTable.insert( std::pair<EdsUInt32, const char *>(0x02,"Face+Tracking"));
	_propertyTable.insert( std::pair<EdsUInt32, const char *>(0x03,"FlexiZone - Multi"));
	_propertyTable.insert( std::pair<EdsUInt32, const char *>(0x04,"Zone AF"));
	_propertyTable.insert( std::pair<EdsUInt32, const char *>(0x05,"Expand AF area"));
	_propertyTable.insert( std::pair<EdsUInt32, const char *>(0x06,"Expand AF area: Around"));
	_propertyTable.insert( std::pair<EdsUInt32, const char *>(0x07,"Large Zone AF: Horizontal"));
	_propertyTable.insert( std::pair<EdsUInt32, const char *>(0x08,"Large Zone AF: Vertical"));
	_propertyTable.insert( std::pair<EdsUInt32, const char *>(0x09,"Catch AF"));
	_propertyTable.insert( std::pair<EdsUInt32, const char *>(0x0a,"Spot AF"));
	_propertyTable.insert( std::pair<EdsUInt32, const char *>(0x0b,"Flexible Zone AF 1"));
	_propertyTable.insert( std::pair<EdsUInt32, const char *>(0x0c,"Flexible Zone AF 2"));
	_propertyTable.insert( std::pair<EdsUInt32, const char *>(0x0d,"Flexible Zone AF 3"));
	_propertyTable.insert( std::pair<EdsUInt32, const char *>(0x0e,"Whole area AF"));
	_propertyTable.insert( std::pair<EdsUInt32, const char *>(0x0f,"No Traking Spot AF"));
	_propertyTable.insert( std::pair<EdsUInt32, const char *>(0x10,"No Traking 1-point AF"));
	_propertyTable.insert( std::pair<EdsUInt32, const char *>(0x11,"No Traking Expand AF area"));
	_propertyTable.insert( std::pair<EdsUInt32, const char *>(0x12,"No Traking Expand AF area: Around"));
	_propertyTable.insert( std::pair<EdsUInt32, const char *>(0xffffffff,"unknown"));
}

CEvfAFMode::~CEvfAFMode()
{
}


BEGIN_MESSAGE_MAP(CEvfAFMode, CPropertyComboBox)
	ON_MESSAGE(WM_USER_PROPERTY_CHANGED, OnPropertyChanged)
	ON_MESSAGE(WM_USER_PROPERTYDESC_CHANGED, OnPropertyDescChanged)
	ON_CONTROL_REFLECT(CBN_SELCHANGE, OnSelChange)
END_MESSAGE_MAP()



// CEvfAFMode message handler
void CEvfAFMode::OnSelChange() 
{
	DWORD_PTR data = GetItemData(GetCurSel());
	
	fireEvent(&data);
}

void CEvfAFMode::update(Observable* from, CameraEvent *e)
{
	std::string event = e->getEvent();

	//Update property
	if(event == "PropertyChanged")
	{
		EdsInt32 propertyID = *static_cast<EdsInt32 *>(e->getArg());
		
		if(propertyID == kEdsPropID_Evf_AFMode)
		{
			//The update processing can be executed from another thread. 
			::PostMessage(this->m_hWnd, WM_USER_PROPERTY_CHANGED, NULL, NULL);
		}
	}
	//Update of list that can set property
	if(event == "PropertyDescChanged")
	{
		EdsInt32 propertyID = *static_cast<EdsInt32 *>(e->getArg());
		
		if(propertyID == kEdsPropID_Evf_AFMode)
		{
			//The update processing can be executed from another thread. 
			::PostMessage(this->m_hWnd, WM_USER_PROPERTYDESC_CHANGED, NULL, NULL);
		}	
	}
}

LRESULT CEvfAFMode::OnPropertyChanged(WPARAM wParam, LPARAM lParam)
{
	updateProperty(getCameraModel()->getEvfAFMode());
	return 0;
}

LRESULT CEvfAFMode::OnPropertyDescChanged(WPARAM wParam, LPARAM lParam)
{
	updatePropertyDesc(&getCameraModel()->getEvfAFModeDesc());
	return 0;
}