using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class InfernoController : MonoBehaviour
{
    // Start is called before the first frame update
    public GameObject extinguisherOnWall;
    public GameObject extinguisherInHand;
    public GameObject player;
    public GameObject wildfire;
    private Vector3 changeInFire;
    void Start()
    {
        // Prepare wildfire but keep it inactive until delay passes
        if (wildfire != null)
        {
            wildfire.transform.localScale = new Vector3(0.2f, 1f, 0.2f);
            wildfire.SetActive(false);
        }
        // start with no growth until fire is enabled
        changeInFire = Vector3.zero;
        extinguisherOnWall.SetActive(true);
        extinguisherInHand.SetActive(false);

        // start wildfire after 5 seconds
        StartCoroutine(StartFireAfterDelay(5f));
    }

    // Update is called once per frame
    void Update()
    {
        wildfire.transform.localScale += changeInFire;

        if (wildfire.transform.localScale.x <= 0.1f && extinguisherInHand.activeSelf)
        {
            wildfire.SetActive(false);
        }
    }

    public void pickupExtinguisher()
    {
        changeInFire -= new Vector3(0.004f, 0, 0.004f);
        extinguisherOnWall.SetActive(false);
        extinguisherInHand.SetActive(true);
    }

    private System.Collections.IEnumerator StartFireAfterDelay(float delay)
    {
        yield return new WaitForSeconds(delay);
        if (wildfire != null)
        {
            wildfire.SetActive(true);
            // start the normal growth rate
            changeInFire = new Vector3(0.002f, 0f, 0.002f);
        }
    }
}
