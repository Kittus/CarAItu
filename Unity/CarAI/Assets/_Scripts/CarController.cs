using UnityEngine;
using System.Collections;
using System.Text;
using System.IO;

public class CarController : MonoBehaviour {
    StreamReader reader;
    public string fileName;
    public float velocity = 1f;
    string line;
    Vector3 objective;
    bool moving;

    public float range = 100f;
    public bool lasers = false;

    LineRenderer gunLine;
    Ray shootRay;
    RaycastHit shootHit;
    int shootableMask;

    public bool finished = false;

    // Use this for initialization
    void Start () {
        reader = new StreamReader(fileName, Encoding.Default);
        gunLine = GetComponent<LineRenderer>();
        shootableMask = LayerMask.GetMask("Shootable");
        gunLine.enabled = true;
        moving = false;
        finished = false;
    }
	
	// Update is called once per frame
	void Update () {
        //Movement Controls
        if (!moving) {
            line = reader.ReadLine();

            if (line != null)
            {
                string[] entries = line.Split(' ');
                if (entries.Length == 3)
                {
                    objective = new Vector3(float.Parse(entries[0]), 0.5f, float.Parse(entries[1]));

                    var rotationVector = transform.rotation.eulerAngles;
                    rotationVector.y = - float.Parse(entries[2])/Mathf.PI * 180 + 90;
                    transform.rotation = Quaternion.Euler(rotationVector);

                    moving = true;
                }
            }
            else
            {
                finished = true;
            }
        }

        if ((objective - gameObject.transform.position).magnitude < velocity)
        {
            gameObject.transform.position = objective;
            moving = false;
        }
        else gameObject.transform.position += (objective - gameObject.transform.position).normalized * velocity;

        //Lasers Plotting
        if (lasers)
        {
            for (int i = 0; i < 11; ++i) gunLine.SetPosition(i, transform.position - new Vector3(0, 0.05f, 0));

            shootRay.origin = transform.position - new Vector3(0, 0.05f, 0);
            shootRay.direction = transform.up;
            if (Physics.Raycast(shootRay, out shootHit, range, shootableMask)) gunLine.SetPosition(1, shootHit.point);
            else gunLine.SetPosition(1, shootRay.origin + shootRay.direction * range);

            shootRay.direction = -transform.right;
            if (Physics.Raycast(shootRay, out shootHit, range, shootableMask)) gunLine.SetPosition(3, shootHit.point);
            else gunLine.SetPosition(3, shootRay.origin + shootRay.direction * range);

            shootRay.direction = transform.right;
            if (Physics.Raycast(shootRay, out shootHit, range, shootableMask)) gunLine.SetPosition(5, shootHit.point);
            else gunLine.SetPosition(5, shootRay.origin + shootRay.direction * range);

            shootRay.direction = Quaternion.Euler(0, 45, 0) * transform.up;
            if (Physics.Raycast(shootRay, out shootHit, range, shootableMask)) gunLine.SetPosition(7, shootHit.point);
            else gunLine.SetPosition(7, shootRay.origin + shootRay.direction * range);

            shootRay.direction = Quaternion.Euler(0, -45, 0) * transform.up;
            if (Physics.Raycast(shootRay, out shootHit, range, shootableMask)) gunLine.SetPosition(9, shootHit.point);
            else gunLine.SetPosition(9, shootRay.origin + shootRay.direction * range);
        }

    }
}
